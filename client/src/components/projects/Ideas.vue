<template>
  <div>
    <Header />
    <div class="w-4/5 m-auto mt-6 text-white">
      <table
        class="w-full border-collapse shadow-lg rounded-lg overflow-hidden bg-card"
      >
        <thead>
          <tr class="bg-bgg text-left">
            <th class="px-6 py-3">#</th>
            <th class="px-6 py-3">Название</th>
            <th class="px-6 py-3">Стеки технологий</th>
            <th class="px-6 py-3">Статус</th>
            <th class="px-6 py-3">Дата создания</th>
            <th class="px-6 py-3"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in items"
            :key="index"
            class="border-b border-zinc-700 hover:bg-card transition duration-200"
          >
            <td class="px-6 py-4">{{ index + 1 }}</td>
            <td class="px-6 py-4 font-medium">{{ item.name }}</td>
            <td class="px-6 py-4">{{ item.description }}</td>
            <td class="px-6 py-4">{{ item.description }}</td>
            <td class="px-6 py-4">
              <span
                v-for="tech in item.technologies"
                :key="tech"
                class="px-2 py-1 bg-purple-600 text-xs rounded mr-1"
              >
                {{ tech }}
              </span>
            </td>
            <td class="px-6 py-4 flex gap-5">
              <button
                @click="toggleLike(item)"
                class="px-4 py-2 text-sm font-medium rounded flex items-center gap-1 transition"
                :class="
                  item.liked
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-gray-600 hover:bg-gray-700'
                "
              >
                ❤️ {{ item.likes }}
              </button>
              <button
                @click="viewItem(item)"
                class="px-4 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 rounded transition"
              >
                Посмотреть
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Header from "@/components/header.vue";

export default {
  components: { Header },
  data() {
    return {
      items: [
        {
          name: "Проект 1",
          description: "Описание проекта",
          technologies: ["Vue", "Tailwind"],
        },
      ],
    };
  },
  methods: {
    editItem(item) {
      alert(`Редактирование: ${item.name}`);
    },
  },
};
</script>
