// Define a new component called button-counter
Vue.component('light-card', {
    props: ['id', 'name', 'channel', 'image', 'state'],
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

            <v-card-actions>
                <span>{{ name }}</span>
                <v-icon v-if="state" v-on:click="light(0)">mdi-eye</v-icon>
                <v-icon v-if="state===false" v-on:click="light(1)">mdi-eye-off</v-icon>
            </v-card-actions>
        </v-card>
    </div>
    `,
    methods: {
        async light(signal) {
            if (signal === 0)
                this.state = false;
            else
                this.state = true;
            
            const url = `api/lights/${this.id}?signal=${signal}`;
            const response = await fetch(url);
            console.log(response);
        }
    }
  })