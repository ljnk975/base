#!/opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: vm.py,v $
# Revision 1.9  2010/06/22 21:42:36  bruno
# power control and console access for VMs
#
# Revision 1.8  2009/05/01 19:07:08  mjk
# chimi con queso
#
# Revision 1.7  2008/10/18 00:56:02  mjk
# copyright 5.1
#
# Revision 1.6  2008/08/22 23:26:38  bruno
# closer
#
# Revision 1.5  2008/04/16 19:11:31  bruno
# only get partition info for partitions that are mountable (i.e., they
# have a leading '/' in the mountpoint field).
#
# Revision 1.4  2008/03/06 23:41:44  mjk
# copyright storm on
#
# Revision 1.3  2008/02/12 00:15:39  bruno
# partition sizes can be reported as floats
#
# Revision 1.2  2008/02/07 20:10:32  bruno
# added some global functions for VM management
#
# Revision 1.1  2008/01/31 20:05:32  bruno
# needed a helper function for the VM configuration rocks command line
#
#

import os
import sys

class VM:

	def __init__(self, db):
		self.db = db
		return


	def partsizeCompare(self, x, y):
		xsize = x[0]
		ysize = y[0]

		suffixes = [ 'KB', 'MB', 'GB', 'TB', 'PB' ]

		xsuffix = xsize[-2:].upper()
		ysuffix = ysize[-2:].upper()

		try:
			xindex = suffixes.index(xsuffix)
		except:
			xindex = -1

		try:
			yindex = suffixes.index(ysuffix)
		except:
			yindex = -1

		if xindex < yindex:
			return 1
		elif xindex > yindex:
			return -1
		else:
			try:
				xx = float(xsize[:-2])
				yy = float(ysize[:-2])

				if xx < yy:
					return 1
				elif xx > yy:
					return -1
			except:
				pass

		return 0


	def getPartitions(self, host):
		partitions = []

		rows = self.db.execute("""select p.mountpoint, p.partitionsize
			from partitions p, nodes n where p.node = n.id and
			n.name = '%s'""" % (host))

		if rows > 0:
			for (mnt, size) in self.db.fetchall():
				if mnt in [ '', 'swap' ]:
					continue
				if len(mnt) > 0 and mnt[0] != '/':
					continue

				partitions.append((size, mnt))

		return partitions


	def getLargestPartition(self, host):
		#
		# get the mountpoint for the largest partition for a host
		#
		maxmnt = None

		sizelist = self.getPartitions(host)
		if len(sizelist) > 0:
			sizelist.sort(self.partsizeCompare)
			(maxsize, maxmnt) = sizelist[0]

		return maxmnt


	def getPhysHost(self, vm_host):
		#
		# get the physical host that controls this VM host
		#
		host = None

		rows = self.db.execute("""select vn.physnode from vm_nodes vn,
			nodes n where n.name = '%s' and n.id = vn.node"""
			% (vm_host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
			rows = self.db.execute("""select name from nodes where
				id = %s""" % (physnodeid))

			if rows == 1:
				host, = self.db.fetchone()

		return host


	def isVM(self, host):
		#
		# a node is a VM if it is in the vm_nodes table
		#
		try:
			rows = self.db.execute("""select n.name from
				nodes n, vm_nodes vn where
				n.name = '%s' and n.id = vn.node""" % host)
		except:
			rows = 0

		return rows

import socket
import sha
import ssl
import M2Crypto
import select

class VMControl:

	def __init__(self, db, me, host):
		self.db = db
		self.me = me
		self.controller = host
		self.port = 8677
		return


	def sendcommand(self, s, op, src_mac, dst_mac):
		msg = '%s\n' % op

		#
		# source MAC
		#
		msg += '%s\n' % src_mac

		if op != 'list macs':
			#
			# destination MAC
			#
			msg += '%s\n' % dst_mac

		#
		# send the size of the clear text and send the clear text
		# message
		#
		s.write('%08d\n' % len(msg))
		s.write(msg)

		#
		# now add the signed digest
		#

		#
		# good key
		#
		key = M2Crypto.RSA.load_key('/tmp/control/private.key')

		digest = sha.sha(msg).digest()
		signature = key.sign(digest, 'ripemd160')

		#
		# send the length of the signature
		#
		s.write('%08d\n' % len(signature))
		s.write(signature)


	def cmd(self, op, host):
		#
		# the list of valid commands:
		#
		#	power off
		#	power on
		#	list macs
		#	console
		#

		#
		# look up the source MAC address -- this is any non-NULL MAC
		# associated with the host.
		#
		rows = self.db.execute("""select mac from networks where
			node = (select id from nodes where name = '%s') and
			mac is not NULL""" % self.me)

		if rows > 0:
			src_mac, = self.db.fetchone()
		else:
			return 'failed'

		#
		# look up the destination MAC address
		#
		rows = self.db.execute("""select mac from networks where
			node = (select id from nodes where name = '%s') and
			mac is not NULL""" % host)

		if rows > 0:
			dst_mac, = self.db.fetchone()
		else:
			return 'failed'

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s = ssl.wrap_socket(sock)
		s.connect((self.controller, self.port))
		
		retval = ''

		if op in [ 'power off', 'power on' ]:
			self.sendcommand(s, op, src_mac, dst_mac)
		elif op == 'list macs':
			#
			# pick up response
			#
			self.sendcommand(s, op, src_mac, dst_mac)

			buf = s.read(9)

			try:
				msg_len = int(buf)
			except:
				msg_len = 0

			macs = ''
			while len(macs) != msg_len:
				msg = s.read(msg_len - len(macs))
			macs += msg

			retval = macs
		elif op == 'console':
			vnc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			#
			# find a free port
			#
			success = 0
			for i in range(1, 100):
				vncport = 5900 + i
				try:
					vnc.bind(('localhost', vncport))
					success = 1
					break
				except:
					pass

			if success == 0:
				return 'failed'

			vnc.listen(1)

			#
			# start the connection
			#
			self.sendcommand(s, op, src_mac, dst_mac)

			pid = os.fork()
			if pid == 0:
				os.system('vncviewer localhost:%d' % vncport)
				os._exit(0)
			else:
				conn, addr = vnc.accept()

				done = 0
				while not done:
					(i, o, e) = select.select(
						[sock.fileno()], [], [],
						0.00001)
					if sock.fileno() in i:
						try:
							output = s.read(65536)
							conn.send(output)
						except:
							done = 1
							continue

					(i, o, e) = select.select(
						[conn.fileno()], [], [],
						0.00001)
					if conn.fileno() in i:
						try:
							input = conn.recv(4096)
							s.write(input)
						except:
							done = 1
							continue

				conn.shutdown(socket.SHUT_RDWR)
				conn.close()

		s.write(' ')
		s.shutdown(socket.SHUT_RDWR)
		sock.shutdown(socket.SHUT_RDWR)
		s.close()
		sock.close()

		return retval
