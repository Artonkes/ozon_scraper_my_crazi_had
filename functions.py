

async def page_down(page):
    await page.evaluate('''
        const scrollStep = 200; // Размер шага прокрутки (в пикселях)
        const scrollInterval = 100; // Интервал между шагами (в миллисекундах)

        const scrollHeight = document.documentElement.scrollHeight;
        let currentPosition = 0;
        const interval = setInterval(() => {
            window.scrollBy(0, scrollStep);
            currentPosition += scrollStep;

            if (currentPosition >= scrollHeight) {
                clearInterval(interval);
            }
        }, scrollInterval);
    ''')