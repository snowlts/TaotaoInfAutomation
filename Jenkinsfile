#!/usr/bin/env groovy
pipeline{
    agent any
    options{
        preserveStashes(buildCount: 10)
    }
    stages{
        stage('deploy taotao project'){
            steps{
                sh 'echo deploy taotao!'
                sh 'echo $WORKSPACE'
                def taotao_dir = sh(script: "dirname $WORKSPACE", returnStdout:true).trim()
                echo "${taotao_dir}"

                dir("${taotao_dir}"){
                    git credentialsId: '381e7be1-1cf0-4a2c-9577-8e4e7ab2026b', url: 'https://gitee.com/snowlts/taotao.git'
                }

                sh 'pip install -r ${taotao_dir}/requirements.txt'
                sh 'python ${taotao_dir}/taotao/manage.py runserver'
                sh 'echo deploy taotao done!'
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
            sh 'report_dir=$WORKSPACE/report/results;if [ ! -e $report_dir ];then mkdir $report_dir;fi'
            allure includeProperties: false, jdk: '', results: [[path: 'report/results']]



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