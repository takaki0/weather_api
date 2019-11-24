<template>
    <div>
        <h1>{{ title }}</h1>
        <h4>
            <a v-github:none.round.shadow.padding="{color: 'green' }">
                github URLはコチラ: https://github.com/takaki0/weather_api
            </a>
        </h4>
    </div>
</template>

<script>
  export default {
    // props: ["applicationVersion"],
    props: {
      applicationVersion: {
        type: String,
        required: false,
        default: 'V.1',
      }
    },
    computed: {
      title() {
        return '気象情報検索 ' + this.applicationVersion;
      },
    },
  };
</script>
