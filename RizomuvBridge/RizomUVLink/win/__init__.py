# MIT License
# 
# Copyright (c) 2022 Rizom-Lab
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Trying python versions from the oldest to the newest
try:
	import win.rizomuvlink_python36 as rizomuvlink
except:
	try:
		import win.rizomuvlink_python37 as rizomuvlink
	except:
		try:
			import win.rizomuvlink_python38 as rizomuvlink
		except:
			try:
				import win.rizomuvlink_python39 as rizomuvlink
			except:
				try:
					import win.rizomuvlink_python310 as rizomuvlink
				except:
					try:
						import win.rizomuvlink_python311 as rizomuvlink
					except:
						try:
							import win.rizomuvlink_python312 as rizomuvlink
						except:
							raise "rizomuvlink version for the current python version not found. Please tell to the Rizom-Lab team which version would you need. We may add it to the list."

