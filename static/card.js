// Define a new component called button-counter
Vue.component('light-card', {
    props: ['name', 'channel', 'image'],
    data: function () {
      return {
        count: 0
      }
    },
    template: `
    <div>
        <v-card
        elevation="2"
            >
            <v-card-title>{{ name }}</v-card-title>
            <v-card-actions>
                <v-btn v-on:click="light(1)">On</v-btn>  
                <v-btn v-on:click="light(0)">Off</v-btn>
            </v-card-actions>
        </v-card>
    </div>
    `,
    methods: {
        async light(signal) {
            const url = `api/light/${this.channel}?signal=${signal}`;
            const response = await fetch(url);
            console.log(response);
        }
    }
  })