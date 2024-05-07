#!/usr/bin/env groovy
pipeline{
    agent any
    options{
        preserveStashes(buildCount: 10)
    }
    stages{
        stage('Build'){
            steps{
                sh 'echo build success!'
            }
        }
        stage('Test'){
            steps{
                echo "test begin"
                sh 'pip install -r requirements.txt'
                sh 'python run.py'
                echo "test end"

            }
        }
    }

    post{
        always{
            echo "build result:$currentBuild.currentResult"
            echo "test finished,please check"
            sh 'echo $WORKSPACE'
            sh 'report_dir=$WORKSPACE/report/report;if [ ! -e $report_dir ];then mkdir $report_dir;fi'
            allure includeProperties: false, jdk: '', results: [[path: 'report/report']]



        }
        success{
            echo "test success"
            deleteDir()

        }
        failure{
            echo "test failed"
        }
        unstable{
            echo "unstable:there are failed testcases"
        }
        changed{
            echo "test status changed"
        }

    }

}