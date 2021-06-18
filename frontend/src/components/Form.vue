<template>
  <form id="subscribe-now">
    <div class="row">
      <div class="col-md-8 col-sm-12">
        <fieldset>
          <input v-if="!shortened_link" type="text" placeholder="Введите ссылку" v-model="original_link" required="">
          <input v-else type="text" v-model="shortened_link" ref="shortened_link" required="">

          <input type="text" style="margin-top: 10px; width:300px;" v-model="subpart" placeholder="Введите свой хеш для сокращенной ссылки">
          <p v-if="exception" style="text-align:left; color:red">{{ exception }}</p>
        </fieldset>
      </div>
      <div class="col-md-4 col-sm-12">
        <fieldset>
          <button v-if="!shortened_link" type="button" class="main-button" @click="shorten_link" v-on:click="$emit('update-list')">Сократить</button>
          <div v-else>
            <button class="btn" type="button" @click="refresh">
              <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAACQUlEQVRIie2VzUuUURSHn3NfxzEnV31AUM1UM6M4pZSLoHWtImgpRZuKhIQwiCBi8IpIIEFR2EIEoaA/oKRFtY6KPhCcaD7UETdRtBq/JnNOC2fMd8Y3J9Cdv9W9573n99xzufe8sKV1JKsn4fStXQCZyJ0fAIcyt/c5Nb7PoDvK0maBrIq+UgpDmWBvwgtgVkaKGJ9/2Pj8w+gyeDzcNy2Gi6DqTtMAaEyULqPOaDRrH8QStvafFTRO2i4VvQcgKteTB+x9r121fLsRmJ/fdthgzqlIB6gfeO2bldOJmP1VAQhn7TEDb4oLAckX4EQmZD95QUqKTsRbMWYE2AvyMBWy11yAxq83Gwr++o8iGnEdgkra5Ofakk39ueogzjugpiC0ZIL2S+mb0br6gXJzABGNaF39wHrmAKmDvaPAIKhjlMsuH9dOst0KkAr1uOLVKDIZPy5i3iqMpUM9R1Yq+F8jL9UGnASAIMHV8Q0DJHbbmeWRNmwKwEtlAMkBxL7b7ZsE0GmAxRmaNwpQ47IXXorSLKLngffVGESz9jHoBXesu9ha5ImrAqUwBLKkIh3RiXhrNQBZmOtUlXR5XFXSsjDX6QIUu+IjUD/GjFQDSTb151RoB8mvwuZVaE829ecqHlTbhyu+3M49L4CTxaTBgvLUH2Ds71WslFezXPPFxhK2djHAXeAqqLO2paoYcza53z5bniLRKfscIBW0ZxDUE1BSeCoeM+pcUvSUQAgou77yc+n34tHxcN80VP6wtlSV/gBJGtMOM1mawwAAAABJRU5ErkJggg=="/>
            </button>
            <button class="main-button" type="button" @click="copy">Копировать</button>
          </div>
        </fieldset>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      shortened_link: '',
      exception: '',
      original_link: '',
      subpart: ''
    }
  },

  methods: {
    refresh() {
      this.shortened_link = '';
      this.original_link = '';
      this.subpart = '';
      this.exception = '';
    },

    async shorten_link() {
      const response = await fetch("http://127.0.0.1:8000/", {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true,
        credentials: 'include',
        body: JSON.stringify({
          original_link: this.original_link,
          subpart: this.subpart,
        }),
      });
      const data = await response.json();
      this.shortened_link = data.shortened_link;
      this.$emit('update-table-data');
    },
    async copy() {
      const shortened_link = this.$refs.shortened_link;
      shortened_link.select();
      document.execCommand("copy");
    },
  }
}
</script>
