loctest=$1
servtest=$(echo -n $loctest | perl -pe 's/\.py$/_server.py/')
sol=$(echo -n $loctest | perl -pe 's/\.py$/_sol.sh/')

doc_cont=$(docker ps | tail -1 | perl -nE 'say((split(/\s+/, $_))[-1])')
doc_pid=$(docker inspect --format="{{.State.Pid}}" $doc_cont)
doc_ip=$(docker inspect --format="{{.NetworkSettings.IPAddress}}" $doc_cont)
echo "Docker container $doc_cont pid $doc_pid ip $doc_ip"

if [ -f $sol ]; then
    sudo cp $sol /proc/$doc_pid/root/home/box
fi
if [ -f $servtest ]; then
    sudo cp $servtest /proc/$doc_pid/root/home/box
fi
ssh root@$doc_ip "rm -rf /home/box/web"
ssh root@$doc_ip "bash /home/box/$sol"
source venv/bin/activate
py.test -s --server=$doc_ip $loctest
