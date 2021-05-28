// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_mode: false,

        // Data items for input mode
        modal_active: "modal",
        new_org_name: "",
        new_org_web : "",
        new_org_description : "",

        // Data items for display
        orgs : [],
        allocations: [
            {
                org_name: "Harmony-at-Home",
                amount: "1000"
            }
        ]
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // Functions for managing org add form.
    app.set_add_status = function(new_status){
        //app.vue.add_mode = new_status;
        app.vue.modal_active = new_status
    };

    app.clear_form = function(){
        app.vue.new_org_name = "";
        app.vue.new_org_web = "";
        app.vue.new_org_description = "";
    };

    app.add_org = function(){
        axios.post(add_org_url,
            {
                name: app.vue.new_org_name,
                web: app.vue.new_org_web,
                description: app.vue.new_org_description
            }
            ).then(function (response){
                app.vue.orgs.push({
                    id: response.data.id,
                    proposed_by: response.data.name,
                    org_name: app.vue.new_org_name,
                    org_web: app.vue.new_org_web,
                    org_description: app.vue.new_org_description,
                    deleteable: true
                });
                app.enumerate(app.vue.orgs);
                app.clear_form();
                app.set_add_status("modal");
            });
    };

    app.delete_org = function(org_idx){
        let id = app.vue.orgs[org_idx].id;
        axios.get(delete_org_url, {params: {id: id}}).then(function(response){
            for (let i = 0; i < app.vue.orgs.length; i++){
                if (app.vue.orgs[i].id === id){
                    app.vue.orgs.splice(i, 1);
                    app.enumerate(app.vue.orgs);
                    break;
                }
            }
        });
    };


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        set_add_status: app.set_add_status,
        clear_form: app.clear_form,

        add_org : app.add_org,
        delete_org: app.delete_org
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(load_orgs_url).then(function(response) {
            app.vue.orgs=app.enumerate(response.data.orgs);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
