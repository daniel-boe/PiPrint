echo Current Directory: $PWD
echo Current User: $USER
cp template.service piprint.service

sed -i "s/<user>/$USER/" piprint.service
sed -i 's,<absolute-path>,'"$PWD"',' piprint.service

sudo mv piprint.service //etc/systemd/system/piprint.service
sudo systemctl start piprint
sudo systemctl enable piprint