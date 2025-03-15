<template>
  <div>
    <Header />
    <table
      class="w-3/5 m-auto border-collapse shadow-lg rounded-lg overflow-hidden"
    >
      <thead class="bg-zinc-800 text-white">
        <tr>
          <th class="p-3 text-left">Название идеи</th>
          <th class="p-3 text-left">Статус</th>
          <th class="p-3 text-left">Дата создания</th>
        </tr>
      </thead>
      <tbody>
        <tr class="bg-cards transition-colors text-white hover:bg-zinc-700">
          <td class="p-3 border-t border-zinc-600"></td>
          <td class="p-3 border-t border-zinc-600"></td>
          <td class="p-3 border-t border-zinc-600"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Header from "@/components/header.vue";

export default {
  components: {
    Header,
  },
};
</script>
