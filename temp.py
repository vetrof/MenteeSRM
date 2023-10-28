[Unit]
Description=Django-Q Cluster Service
After=network.target
[Service]
User=vetrof
WorkingDirectory=/home/vetrof/django
ExecStart=/home/vetrof/django/venv/bin/python /home/vetrof/django/manage.py qcluster
Restart=always
[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable qcluster
sudo systemctl start qcluster
sudo systemctl status qcluster
sudo nano /etc/systemd/system/qcluster.service

sudo nano /etc/systemd/system/qcluster.service