set PYTHONIOENCODING=utf-8
echo I:\anaconda3\python.exe
path I:\anaconda3\;I:\Anaconda3\Library\bin;%PATH%
cd /d %~dp0
python main.py  --targets "bc_cezhi bc_zczh" --count_point "bc_cezhi"
cmd

