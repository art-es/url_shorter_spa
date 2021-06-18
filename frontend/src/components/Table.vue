<template>
  <div>
    <table class="table" style="margin-top: 10px;">
      <thead>
        <tr>
          <th scope="col">Original URL</th>
          <th scope="col">Shorten URL</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(shortened_link, index) in shortened_links" :key="index">
          <td>{{ shortened_link.original_link }}</td>
          <td>{{ shortened_link.full_link }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <span class="step-links">
        <button 
          class="btn" 
          :class="page <= 1 ? 'disabled' : ''" 
          :disabled="page <= 1" 
          @click="prevPage"
        >&laquo; previous</button>
        <span class="current">
         {{ page }}
        </span>
        <button 
          class="btn"
          :class="page >= total_pages ? 'disable' : ''"
          :disabled="page >= total_pages"
          @click="nextPage"  
        >next &raquo;</button>
      </span>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      page: 1,
      shortened_links: [],
      total_pages: 0,
    }
  },
  methods: {
    async update_table_data() {
      const response = await fetch(`http://127.0.0.1:8000/?page=${this.page}`, {
        mode: 'cors',
        credentials: 'include',
      });
      const data = await response.json();
      this.shortened_links = data.shortened_links;
      this.total_pages = data.total_pages;
    },

    prevPage() {
      this.page--;
      this.update_table_data();
    },

    nextPage() {
      this.page++;
      this.update_table_data();
    },
  },

  mounted() {
    this.update_table_data();
  }
}
</script>
