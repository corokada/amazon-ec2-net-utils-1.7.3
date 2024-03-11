#
yum -y install git make systemd systemd-units rpm-build

#
git clone https://github.com/corokada/amazon-ec2-net-utils-1.7.3
cd amazon-ec2-net-utils-1.7.3/
rpmbuild --define "_sourcedir $PWD" -bb amazon-ec2-net-utils.spec

#
yum localinstall ~/rpmbuild/RPMS/noarch/amazon-ec2-net-utils-1.7.3-1.el7.noarch.rpm
