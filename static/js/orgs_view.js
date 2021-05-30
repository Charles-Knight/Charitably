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
        allocations: []
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.orgs_in_allocations = () => {
        for (i = 0; i < app.vue.orgs.length; i++) {
            app.vue.orgs[i].in_allocations = app.in_allocations(app.vue.orgs[i].id);
        }
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

    // Functions that operate on organizations
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

    // Remove organization from the database and from the organiztions list view
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

    // Functions to operate on allocations

    // Iterates over the list of allocations to see if the org_id is
    // already present
    app.in_allocations = function(org_id) {
        for (let i = 0; i < app.vue.allocations.length; i++){
            if ( app.vue.allocations[i].org_id === org_id){
                return true;
            }
        }
        return false;
    }
    
    // Allows the user to add an organizations from the organizations list to the allocations list
    app.add_to_allocations = function(org_idx){
        // Get the organization id.
        let org_id = app.vue.orgs[org_idx].id;
        let org_name = app.vue.orgs[org_idx].org_name;

        console.log(org_id)
        console.log(app.in_allocations(org_id))

        if (!app.in_allocations(org_id)){
            app.vue.allocations.push({
                org_id: org_id,
                org_name: org_name,
                amount: 0 
            });
            app.enumerate(app.vue.allocations);
            app.orgs_in_allocations();
        }
    };

    // Remove an allocation from the allocations list
    app.remove_from_allocations = function (allocation_idx){
        let id = app.vue.allocations[allocation_idx].id;
        // TODO: insert API call to update DB

        for (let i = 0; i < app.vue.allocations.length; i++){
            if (app.vue.allocations[i].id === id){
                app.vue.orgs.splice(i, 1);
                app.enumerate(app.vue.allocations);
                app.orgs_in_allocations();
                break;
            }
        }        
    };

    // Clears the allocations list
    app.clear_allocations = function(){
        app.vue.allocations = [];
        app.orgs_in_allocations();
    };


    // This contains all the methods.
    app.methods = {
        // Functions for add orgs form
        set_add_status: app.set_add_status,
        clear_form: app.clear_form,

        // Functions for org management
        add_org : app.add_org,
        delete_org: app.delete_org,

        // Functions for allocations
        add_to_allocations: app.add_to_allocations,
        remove_from_allocations: app.remove_from_allocations,
        clear_allocations: app.clear_allocations,
        in_allocations: app.in_allocations

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
            app.orgs_in_allocations();
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
