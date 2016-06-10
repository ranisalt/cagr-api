import argparse
import asyncio
import hub
import web


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int)
args = parser.parse_args()

app = web.create_app()
web.run_app(app, port=args.port)
