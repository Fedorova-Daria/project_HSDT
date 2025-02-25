<template>
  <div>
    <header class="flex justify-between border-b border-zinc-700">
      <div class="flex items-center gap-4 p-2 ml-auto">
        <ul class="flex items-center gap-10">
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Биржа</button>
          </li>
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Команды</button>
          </li>
          <li
            class="flex items-center gap-3 text-white hover:text-purple-400 duration-500"
          >
            <button>Идеи</button>
          </li>
        </ul>
        <img src="/notific.svg" alt="notification" class="w-10 ml-5" />
      </div>
    </header>
    <h1 class="font-display w-4/5 m-auto mt-20 text-white text-5xl">
      Биржа проектов ВШЦТ
    </h1>
    <div class="flex jusity-between w-4/5 m-auto mt-50">
      <div class="relative">
        <img class="absolute left-2 top-2" src="/search.svg" />
        <input
          class="border bg-white rounded-md py-2 pl-10 pr-4 outline-none focus:border-fiol duration-500"
          type="text"
          placeholder="Поиск..."
        />
      </div>
      <select
        class="ml-5 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все статусы идей</option>
        <option>Набор открыт</option>
        <option>Набор закрыт</option>
      </select>
      <select
        class="ml-5 py-2 px-3 border bg-white rounded-md focus:border-fiol duration-500"
      >
        <option>Все стеки технологий</option>
        <option>Которые я знаю</option>
        <option>Остальные стеки...</option>
      </select>
    </div>
    <div
      class="w-4/5 m-auto rounded-xl mt-5 border-2 border-solid border-zinc-700"
    >
      <div
        class="text-white relative bg-cards rounded-xl p-5 w-130 ml-5 mt-5 mb-5 border border-cards shadow-xl hover:border-fiol duration-300"
      >
        <div class="mb-3 flex jusiify-between">
          <h1 class="text-2xl">
            Создание сайта для проведение конкурса"Педагог года"
          </h1>
          <img src="/liked.svg" alt="Like 1" class="mb-5" />
        </div>
        <h2 class="mb-3 text-gray-200">
          Разработка веб-приложения для создания анкет преподавателей и
          проведения голосования за них...
        </h2>
        <h3 class="mb-3 text-xl">Инициатор: Екатерина Сердюкова</h3>
        <div class="flex gap-3">
          <h1 class="p-2 bg-green-500 rounded-md">C#</h1>
          <h1 class="p-2 bg-green-500 rounded-md">C#</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script></script>
