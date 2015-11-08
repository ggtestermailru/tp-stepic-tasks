loctest=$1
servtest=$(echo -n $loctest | perl -pe 's/\.py$/_server.py/')

doc_cont=$(docker ps | tail -1 | perl -nE 'say((split(/\s+/, $_))[-1])')
doc_pid=$(docker inspect --format="{{.State.Pid}}" $doc_cont)
doc_ip=$(docker inspect --format="{{.NetworkSettings.IPAddress}}" $doc_cont)
echo "Docker container $doc_cont pid $doc_pid ip $doc_ip"

if [ -f $servtest ]; then
    sudo cp $servtest /proc/$doc_pid/root/home/box
fi
source venv/bin/activate
py.test -s --server=$doc_ip $loctest
