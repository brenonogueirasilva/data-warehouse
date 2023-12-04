from dbt.cli.main import dbtRunner, dbtRunnerResult

dbt = dbtRunner()

def main(request):
    def execute_commands_dbt(cli_args):
        
        res: dbtRunnerResult = dbt.invoke(cli_args)
        for r in res.result:
            print(f"{r.node.name}: {r.status}")

    cli_args_run = ["run", "--profiles-dir",  "./dw_olist", "--project-dir" , "./dw_olist", "--select", "dim_city" ]
    cli_args_snapshot = ["snapshot", "--profiles-dir",  "./dw_olist", "--project-dir" , "./dw_olist"]
      
    execute_commands_dbt(cli_args_run)
    execute_commands_dbt(cli_args_snapshot)
    return 'DBT Commands Executed with Sucess'


    

