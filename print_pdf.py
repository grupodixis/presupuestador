from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file:///C:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0020-puertas-acciona/presupuesto-cliente.html")
        page.pdf(path="C:/Users/pablo/Documents/Presupuestador/presupuestos/P-2026-0020-puertas-acciona/presupuesto-cliente-v3.pdf", format="A4", margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, print_background=True)
        browser.close()

if __name__ == "__main__":
    run()
