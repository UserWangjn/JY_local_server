#!/usr/bin/env python

import os, sys, re
import rsync

PROJECTPATH = '/home/admin/code/v2/'
DESTPATH = '/var/www/html/coin/'

PROJECTS = {
           'okcoin-okex':('okcoin-okex','okcoin-okex-web/target/okcoin-okex.jar'),
           'okcoin-trade':('okcoin-trade','okcoin-trade-boot/target/okcoin-trade-boot-*.jar'),
           'okcoin-push':('okcoin-push','target/okcoin-push-*.jar'),
	   'okcoin-scheduler':('okcoin-spot/okcoin-spot-scheduler','target/okcoin-scheduler-*.jar'),
	   'okcoin-spot':('okcoin-spot','okcoin-spot-rest/target/okcoin-spot-*.jar'),
           'okcoin-spot-openrest':('okcoin-spot/okcoin-spot-openrest','target/okcoin-spot-openrest-*.jar'),
           'okcoin-support':('okcoin-support','okcoin-support-rest/target/okcoin-support-*.jar'),
           'okcoin-boss':('okcoin-boss','okcoin-boss-rest/target/okcoin-boss-*.jar'),
           'okcoin-boss-user-rights':('okcoin-boss/okcoin-boss-user-rights','target/okcoin-boss-user-rights-*.jar'),
	   'okcoin-boss-work-order':('okcoin-boss/okcoin-boss-work-order','target/okcoin-boss-work-order-*.jar'),
           'okcoin-auth':('okcoin-auth','okcoin-auth-service/target/okcoin-auth-*-SNAPSHOT.jar'),
           'okcoin-c2c':('okcoin-c2c','target/okcoin-c2c-*.jar'),
           'okcoin-asset':('okcoin-asset','okcoin-asset-rest/target/okcoin-asset-*.jar'),
	   'okcoin-users':('okcoin-users','okcoin-users-rest/target/okcoin-users-*.jar'),
	   'okcoin-users-scheduler':('okcoin-users/okcoin-users-scheduler','target/okcoin-users-scheduler-*.jar'),
	   'okcoin-springcloud-eureka':('okcoin-springcloud-eureka','target/eurekaserver-*.jar'),
	   'okcoin-futures':('okcoin-futures','okcoin-futures-rest/target/okcoin-futures-*.jar'),
	   'okcoin-futures-scheduler':('okcoin-futures/okcoin-futures-scheduler','target/okcoin-futures-scheduler-*.jar'),
	   'okcoin-c2c-open':('okcoin-c2c-open','target/okcoin-c2c-open-*.jar'),
	   'okcoin-market':('okcoin-market','okcoin-market-rest/target/okcoin-market-*.jar'),
	   'okcoin-market-data':('okcoin-market-data','okcoin-market-task/target/okcoin-market-data-*.jar'),
           'okcoin-web':('okcoin-web','target/okcoin-web-*.jar'),
           'okcoin-kr-web':('okcoin-kr-web','target/okcoin-kr-web-*.jar'),
           'okcoin-market-scheduler':('okcoin-market/okcoin-market-scheduler','target/okcoin-market-scheduler-*.jar'),
           'okex-web':('okex-web','target/okex-web-*.jar'),
           'okcoin-ex-wallet':('okcoin-ex-wallet','wallet-web/target/okcoin-ex-wallet-*.jar'),
	   'okcoin-vault':('okcoin-vault','vault-web/target/vault-web-*.jar'),
           'okcoin-npush':('okcoin-npush','target/okcoin-npush-*.jar'),
           'okcoind':('okcoind','target/okcoind/okcoind.jar'),
	   'okcoin-wallet':('okcoin-wallet','okcoin-wallet-service/target/okcoin-wallet-service.jar'),
	   'okcoin-okex-scheduler-admin':('okcoin-okex-scheduler-admin','okcoin-okex-job-admin/target/okcoin-okex-scheduler-admin-*.jar'),
	   'okcoin-futures-trade':('okcoin-futures/okcoin-futures-trade','target/okcoin-futures-trade-*.jar'),
	   'signature-server':('okcoin-signature','signature-server/target/signature-server-*.jar'),
	   'signature-client':('okcoin-signature','signature-client/target/signature-client-*.jar'),
	   'vault-job':('okcoin-vault','vault-job/target/vault-job-*.jar'),
           'okcoin-etf':('okcoin-etf','okcoin-etf/target/okcoin-etf-*.jar')
}


def gitUpdate(path, src, tag):
        print('*** running git update... ***')
        os.system('cd ' + path + ' && git fetch && git checkout ' + tag + '  && git pull origin ' + tag )
#        if tag != 'master':
#                result = os.popen('cd ' + path + ' && git log origin/master ^origin/' + tag + '|wc -l').read().strip('\n')
#                if result != '0':
#                        print('%s do not contain the lates master' %tag)
#                        sys.exit(3)
        print('*** git update finished! ***')
        return 1;

def build(path, site):
        antval = '/usr/local/maven/bin/mvn -f %s/pom.xml clean install -Dmaven.test.skip=true -P%s_docker ' % (path, site)
        result = os.popen(antval).read()
        successPattern = re.compile('BUILD SUCCESS')
        if successPattern.search(result):
                print('*** building complete! ***')
        else:
                print('*** rebuilding failed! ***')
		print(result)
                sys.exit(3)


def usage():
        print('Usage:', sys.argv[0], 'projectnames', 'tag', 'site')
def usage():
        print('Accepted project name is one of followed: okcoin-okex')

def main(argv):
        tag = 'develop'
        if len(argv) < 2:
                usage()
                sys.exit(1)
        elif len(argv) == 4:
                tag = argv[2]

        projName = argv[1]
        site = argv[3]
	if site == 'com' and (projName == 'okcoin-spot' or projName == 'okcoin-support' or projName == 'okcoin-asset' or projName == 'okcoin-users' or projName == 'okcoin-scheduler' or projName == 'okcoin-spot-openrest' ):
		PROJECTPATH = '/home/admin/code/v2_com/'
	else:
		PROJECTPATH = '/home/admin/code/v2/'


        if projName in list(PROJECTS.keys()):
                (src, target) = PROJECTS[projName]
        else:
                print('Project name wrong!')
                usage()
                sys.exit(2)

        projPath = os.path.abspath(PROJECTPATH + src)

        if gitUpdate(projPath, src, tag):
                print('*** building start! ***')
                build(projPath, site)
        else:
                print('*** rebuilding skipped ***')


        print('**********************************************')
        print('*** start rsync all filess *******************')
        print('**********************************************')
        runningPath = os.path.dirname(os.path.abspath(sys.argv[0]))
        exclude = runningPath + '/' +projName
        xclude = {'exclude':exclude, }

        rs = rsync.Rsync(projPath + '/' + target, DESTPATH + site + '/' + projName + '.jar', '-auzv --delete -e ssh', xclude)
        '/home/admin/code/v2/okcoin-etf/'
        print(rs.list())
        rs.run()

if __name__=='__main__':
        main(sys.argv)