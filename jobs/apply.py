from playwright.sync_api import sync_playwright, Page, BrowserContext
from subprocess import run
from time import sleep, time
from bs4 import BeautifulSoup, element
from openai import OpenAI
from textwrap import dedent

interactive_html = ["input", "button", "a", "radio"]
client = OpenAI(api_key="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")
GPT3 = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4-1106-preview"
pricing = {
    GPT3: 0.001,
    GPT4: 0.01,
}


def main():
    run(["open", "-a", "Google Chrome", "--args", "--remote-debugging-port=9222"])
    sleep(0.5)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        test(context)


def test(context: BrowserContext):
    page = context.pages[0]
    page.goto(
        "https://boards.greenhouse.io/ninjatrader/jobs/4312933006?gh_src=39e2b8c16us"
    )
    form_filler(page)


def apply_seek(context: BrowserContext):
    page = context.pages[0]
    seek_id = 71660964
    page.goto(f"https://seek.com/job/{seek_id}")
    page.locator('[data-automation="job-detail-apply"]').click()
    sleep(1)
    pages = get_pages(context)
    if len(pages) > 1:
        return form_filler(pages[-1])

    page.get_by_label("Don't include a cover letter").click()
    page.get_by_label("Continue").click()


def form_filler(page: Page):
    sleep(2)
    print("current job url:", get_url(page))
    fill_inputs(page)
    fill_selects(page)
    upload_resume(page)
    continue_submit(page)


def fill_inputs(page):
    for element_type in ["input", "textarea"]:
        for tag in get_html_body(page).find_all(element_type):
            fill_input(tag, page)


def fill_input(tag: element.Tag, page: Page):
    label = find_input_label(tag)
    el = page.locator(xpath(tag))
    if label:
        print('\n\n')
        print(label)
        print(tag)


def find_input_label(tag: element.Tag):
    label = list(tag.find_all("label"))
    if len(label) == 1:
        return label[0]

    if label:
        return

    return find_input_label(tag.parent)


def upload_resume(page):
    pass


def continue_submit(page):
    return


def fill_selects(page):
    pass


def get_html_body(page: Page):
    html = BeautifulSoup(page.content(), features="lxml")
    return html.find("body")


def get_pages(context: BrowserContext):
    context.new_page().close()  # hack to work around the bug where pages never gets updated with the latest
    return context.pages


def get_url(page: Page):
    return page.evaluate("() => window.location.href")


def gpt(msg, system_msg="answer only with y or n", model=GPT3):
    messages = [{"role": "user", "content": msg}]
    if system_msg:
        messages = [
            {"role": "system", "content": system_msg},
        ] + messages
        
    response = client.chat.completions.create(
        temperature=0,
        model=model,
        messages=messages,
    )
    tokens = response.usage.total_tokens
    cost = round(pricing[model] * tokens / 1000, 5)
    print(f"cost: ${cost}")
    return response


def xpath(element: element.Tag | element.NavigableString) -> str:
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if 1 == len(siblings)
            else "%s[%d]"
            % (child.name, next(i for i, s in enumerate(siblings, 1) if s is child))
        )
        child = parent

    components.reverse()
    return "xpath=//" + "/".join(components)


if __name__ == "__main__":
    main()
