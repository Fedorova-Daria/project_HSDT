module.exports = {
    // Активируем поддержку тем через классы
    darkMode: 'class', // Установка класса для управления темой (light/dark)

    // Пути к файлам, где используется Tailwind
    content: [
      './src/**/*.{html,js,vue}', // Настройте путь к вашим HTML, JS и Vue-файлам
      './index.html',      // Если есть HTML в public
    ],

    // Настройка тем и кастомных параметров
    theme: {
        extend: {
            colors: {
                lightBackground: '#ffffff',
                darkBackground: '#141414',
                lightText: '#000000',
                darkText: '#e0e0e0',
                primary: '#007bff',
                secondary: '#66b2ff',
            },
                transitionDuration: {
                DEFAULT: '300ms',
            },
        },
    },
    // Настройки плагинов, если они нужны
    plugins: [],
};