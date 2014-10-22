GENERAL_LOG = 'ett_network_building_log.txt'
def write_and_close(s):
    print s
    f = open(GENERAL_LOG, 'a')
    f.write(s + '\n')
    f.close()
