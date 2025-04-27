




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":


    run_info = RunInfo(
        code_str="""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT
);

INSERT INTO users (name, age) VALUES ('Alice', 23), ('Bob', 30);

DROP TABLE users;
""",
        language="sql",
        project_root_name="project_sql",
        delete_after_run=False,
    )
    run_info.print_tree()




    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    print(result_info.stdout.decode())
    a=1