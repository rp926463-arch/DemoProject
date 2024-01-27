import kazoo
import logging
import utils.zookeeper_python as zookeeper_python

logger = logging.getLogger(__name__)


def initiateZkConn(environment, node):
    try:
        region = environment
        if region != "Failure" and region is not None and region != "":
            zk = zookeeper_python.getKazooClient(region, node)
            return zk
        else:
            logger.error(f'Process to fetch Environment has failed. Terminating the request to fetch environment')
            return "Failure"
    except Exception as zkConnErr:
        logger.error(f'Process to initiate ZK connection has failed with error - {zkConnErr}')
        return "Failure"


def fetchZkNode(zkpath=None, environment=None, node=None):
    try:
        zk = initiateZkConn(environment, node)

        if zk != "Failure" and zkpath != "" and zkpath is not None:
            zk.start()
            zkNodeValue, zkStats = zk.get(f'{zkpath}') if zkpath.startswith('/') else zk.get(f'/{zkpath}')
            logger.info(f'Zookeeper node deatils of {node}/{zkpath} has been fetched successfully and the node deatils '
                        f'are - {zkNodeValue.decode("utf-8")}')
            zk.stop()
            return zkNodeValue.decode("utf-8")
        else:
            raise Exception(f'Either ZK Node is not available or ZK path is not passed as one of the input parameter.')
    except kazoo.exceptions.NoNodeError:
        raise Exception(f'Process to list XK node - {zkpath} has failed with \'NoNodeError\'')
    except Exception as fetchZkNodeErr:
        zk.stop()
        raise Exception(f'Process to list the ZK node - {zkpath} has failed with error - {fetchZkNodeErr}')
