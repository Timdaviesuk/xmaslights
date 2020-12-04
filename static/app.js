new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        lights: [],
    },
    methods: {
        async getLights() {
            const url = `api/lights`;
            const response = await fetch(url);
            this.lights = await response.json();
            this.updateState();
        },
        async updateState() {
            const url = `api/lights`;
            const response = await fetch(url);
            const lightStates = await response.json();
            
            lightStates.forEach(l => {
                // Get the light
                const light = this.lights.find((ll) => ll.id === l.id);
                light.state = l.state;
            });
        }
    },
    async mounted() {
        await this.getLights();
        setInterval(this.updateState, 2000)
    }
})