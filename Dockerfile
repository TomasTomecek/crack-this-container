FROM fedora:25
RUN dnf install -y openssh-server
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa && \
	ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
COPY files/bashrc /root/.bashrc
COPY files/sshd_config /etc/ssh/
# generated with ssh-keygen -b 4096 -t rsa -f ./id_rsa
COPY files/id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 0600 /root/.ssh/authorized_keys
CMD ["/usr/sbin/sshd", "-D"]
