import typer

from agentx.seo import analyze_seo, get_keyword_suggestions, optimize_metadata
from agentx.performance import monitor_api, log_performance
from agentx.scraper import scrape_website
import click
import subprocess
import time

app = typer.Typer()

@app.command()
def optimize(url: str = typer.Argument(..., help="The URL of the webpage to optimize")):
    """
    Optimize SEO for the provided webpage URL.
    """
    typer.echo("Running SEO Optimization and Performance Monitoring...")

    url = "https://ayushhh.medium.com/summer-of-bitcoin23-my-experience-1357a0f16495"
    
    typer.echo(f"\nVisit this site: http://localhost:5000/seo?url={url}\n")

    # seo_report = analyze_seo(url)
    # typer.echo(f"SEO Report: {seo_report}")
    
    # keyword_data = get_keyword_suggestions(url)
    # typer.echo(f"Keyword Suggestions: {keyword_data}")
    
    # current_html = "<html>... current metadata ...</html>"
    # optimized_html = optimize_metadata(current_html)
    # typer.echo("Optimized Metadata:")
    # typer.echo(optimized_html)
    
    # Monitor and log API performance
    performance_report = monitor_api()
    log_performance(performance_report)
    # typer.echo("Performance data logged.")

@app.command()
def scrape():

    url = typer.prompt("Enter the website URL")

    typer.echo("Ensuring Playwright browsers are installed...")
    try:
        subprocess.run(["playwright", "install"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo("Failed to install Playwright dependencies.")
        raise e

    try:
        process = subprocess.Popen(["python", "api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except Exception as e:
        typer.echo(f"Failed to start the API server: {e}")
        raise e

    time.sleep(2)
    
    typer.echo("Flask API server started in the background.")
    typer.echo(f"Access the scraped JSON at: http://127.0.0.1:5000/scrape?url={url}")
    typer.echo("Press Ctrl+C to exit and stop the API server.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Exiting CLI and terminating API server...")
        process.terminate()
        process.wait()


@app.command()
def brokenlink():

    url = typer.prompt("Enter the website URL")

    try:
        process = subprocess.Popen(["python", "api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except Exception as e:
        typer.echo(f"Failed to start the API server: {e}")
        raise e

    time.sleep(2)
    
    typer.echo("Flask API server started in the background.")
    typer.echo(f"Access the scraped JSON at: http://127.0.0.1:5000/errorlink?url={url}")
    typer.echo("Press Ctrl+C to exit and stop the API server.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Exiting CLI and terminating API server...")
        process.terminate()
        process.wait()



@app.command()
def fix_errors():
    url = typer.prompt("Enter the website URL")
    try:
        process = subprocess.Popen(["python", "api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except Exception as e:
        typer.echo(f"Failed to start the API server: {e}")
        raise e

    time.sleep(2)
    
    typer.echo("Flask API server started in the background.")
    typer.echo(f"Access the scraped JSON at: http://127.0.0.1:5000/update?url={url}")
    typer.echo("Press Ctrl+C to exit and stop the API server.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Exiting CLI and terminating API server...")
        process.terminate()
        process.wait()


@app.command()
def generate_content():
    url = typer.prompt("Enter the website URL")
    try:
        process = subprocess.Popen(["python", "api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except Exception as e:
        typer.echo(f"Failed to start the API server: {e}")
        raise e

    time.sleep(2)
    
    typer.echo("Flask API server started in the background.")
    typer.echo(f"Access the scraped JSON at: http://127.0.0.1:5000/add?url={url}")
    typer.echo("Press Ctrl+C to exit and stop the API server.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("Exiting CLI and terminating API server...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    app()
