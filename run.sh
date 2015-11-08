doc_cont=$(docker ps | tail -1 | perl -nE 'say((split(/\s+/, $_))[-1])')
doc_pid=$(docker inspect --format="{{.State.Pid}}" $doc_cont)
doc_ip=$(docker inspect --format="{{.NetworkSettings.IPAddress}}" $doc_cont)
echo "Docker container $doc_cont pid $doc_pid ip $doc_ip"

sudo cp solution.sh /proc/$doc_pid/root/home/box
sudo cp server_*.py /proc/$doc_pid/root/home/box

ssh root@$doc_ip "rm -rf /home/box/web"
ssh root@$doc_ip "/home/box/solution.sh"

source venv/bin/activate

if [ -z "$1" ]; then
    py.test -s --server=$doc_ip test_*.py
else
    py.test -s --server=$doc_ip $1
fi
