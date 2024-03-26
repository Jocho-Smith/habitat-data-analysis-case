.PHONY: run stop

run:
        tmux new-session -d -s my_session 'source env/bin/activate && python scrape.py'

stop:
        tmux kill-session -t my_session

