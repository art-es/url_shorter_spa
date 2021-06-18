<template>
  <div id="app">
    <section class="section" id="subscribe">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 offset-lg-2">
            <div class="section-heading">
              <h2>Сокращатель URL-адресов</h2>
            </div>
            <div class="subscribe-content">
              <p>Вы просто вводите необходимый длинный URL в поле ввода и получаете его короткий аналог.</p>
              <div class="subscribe-form">
                <Form @update-table-data="$refs.table_data.update_table_data()" />
                <Table ref="table_data" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Form from './components/Form.vue'
import Table from './components/Table.vue'

export default {
  name: 'App',

  components: {
    Form,
    Table,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
