import asyncio
import nest_asyncio
from pyppeteer import launch
from urllib.parse import urlparse, parse_qs, unquote, urljoin

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()
executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # ADJUST THIS PATH!
selected_div_info = []

async def main():
    browser = await launch(
        executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # YOUR CHROME PATH
        headless=False  # You need to see the browser to select text
    )
    page = await browser.newPage()

    # Python function to be called from JavaScript
    def python_log_selection(class_name, selected_text):
        print(f"[PYTHON] User selected text: '{selected_text}'")
        print(f"[PYTHON] Class name of containing div: '{class_name}'")
        selected_div_info.append({'class': class_name, 'text': selected_text})
        # In a real app, you might put this into an asyncio.Queue
        # await queue.put({'class': class_name, 'text': selected_text})

    # Expose the Python function to the page under the name 'pyLogSelection'
    await page.exposeFunction('pyLogSelection', python_log_selection)

    await page.goto('https://shop.kimelo.com/department/cheese/3365')  # Example page

    # Inject JavaScript to listen for text selection
    await page.evaluate('''() => {
        document.addEventListener('mouseup', () => {
            const selection = window.getSelection();
            const selectedText = selection.toString().trim();

            if (selectedText.length > 0) {
                let anchorNode = selection.anchorNode; // Start of selection
                let focusNode = selection.focusNode;   // End of selection

                // Try to find a common ancestor or the node itself if it's an element
                let commonAncestor = selection.getRangeAt(0).commonAncestorContainer;
                if (commonAncestor.nodeType === Node.TEXT_NODE) {
                    commonAncestor = commonAncestor.parentElement;
                }

                let targetDiv = commonAncestor;
                let currentNode = commonAncestor;

                let className = 'N/A';
                if (targetDiv && targetDiv.className) {
                    if (typeof targetDiv.className === 'string') {
                         className = targetDiv.className;
                    } else if (typeof targetDiv.className === 'object' && targetDiv.className.baseVal) {
                        // For SVGAnimatedString objects (like on some SVG elements)
                        className = targetDiv.className.baseVal;
                    }
                }

                // Call the exposed Python function
                window.pyLogSelection(className, selectedText);
            }
        });
        console.log('Text selection listener attached.');
    }''')

    print("JavaScript listener injected. Try selecting some text on the page.")
    print("Press Ctrl+C in this terminal to close the browser and exit.")

    # Keep the script running so the browser stays open
    # and the event listener can work.
    try:
        for i in range(30):
            await asyncio.sleep(1)
            # You could periodically check selected_div_info here if not using a queue
    except KeyboardInterrupt:
        print("Closing browser...")
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
    print("Final selected div info captured in Python:", selected_div_info)