// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.

        // Data items for group input 
        modal_active: "modal",
        drop_active: "dropdown",
        new_group_name: "",
        new_funding_amount : "",
        new_group_desc : "",

        // Data items for new member input
        member_modal: "modal",
        new_member_email: "",
        new_member_role: "",

        // Data items for display
        groups : [],
        selected_group_members: [],
        selected_group_id: "",
        selected_group_name: "",
        selected_group_desc: "",
        selected_group_funding: "",
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    // Functions for managing group creation form.
    app.set_add_status = function(new_status){
        //app.vue.add_mode = new_status;
        app.vue.modal_active = new_status
    };

    app.clear_form = function(){
        app.vue.new_group_name = "";
        app.vue.new_funding_amount = "";
        app.vue.new_group_desc = "";
    };

    // Function to toggle group selection dropdown
    app.toggle_drop = function(){
        if (app.vue.drop_active === "dropdown"){
            app.vue.drop_active = "dropdown is-active"
        } else {
            app.vue.drop_active = "dropdown"
        }
    };

    // Functions that operate on groups
    app.create_group = function(){
        axios.post(create_group_url,
            {
                group_name: app.vue.new_group_name,
                group_desc: app.vue.new_group_desc,
                funding: app.vue.new_funding_amount,

            }).then(function (response){
                app.vue.groups.push({
                    id: response.data.id,
                    group_name: app.vue.new_group_name,
                    group_desc: app.vue.new_group_desc,
                    funding: app.vue.new_funding_amount,
                });
                app.enumerate(app.vue.groups);
                app.clear_form();
                app.set_add_status("modal");
            });
    };

    app.select_group = function(idx){
        console.log("Selected Group");
        app.vue.selected_group_id = app.vue.groups[idx]['id'];
        app.vue.selected_group_name = app.vue.groups[idx]['group_name'];
        app.vue.selected_group_desc = app.vue.groups[idx]['group_desc'];
        app.vue.selected_group_funding = app.vue.groups[idx]['funding'];
        app.toggle_drop();

        // TODO: Load selected group members
    };

    app.toggle_add_member = function(){
        if (app.vue.member_modal === "modal" && app.vue.selected_group_id != ""){
            app.vue.member_modal = "modal is-active";
        } else {
            app.vue.member_modal = "modal";
        }
    };

    app.clear_add_member = function(){
        app.vue.new_member_email = "";
        app.vue.new_member_role = "";
    }

    app.add_member = function(){
        axios.post(add_group_member_url,
            {
                group_id: app.vue.selected_group_id,
                email: app.vue.new_member_email,
                role: app.vue.new_member_role,
            }).then(function (response){
                app.vue.selected_group_members.push({
                    id: id
                });
                app.clear_add_member();
            });
        
    }

    // Remove organization from the database and from the organiztions list view
    // app.delete_org = function(org_idx){
    //     let id = app.vue.orgs[org_idx].id;
    //     axios.get(delete_org_url, {params: {id: id}}).then(function(response){
    //         for (let i = 0; i < app.vue.orgs.length; i++){
    //             if (app.vue.orgs[i].id === id){
    //                 app.vue.orgs.splice(i, 1);
    //                 app.enumerate(app.vue.orgs);
    //                 break;
    //             }
    //         }
    //     });
    // };


    // This contains all the methods.
    app.methods = {
        // Functions for add orgs form
        set_add_status: app.set_add_status,
        clear_form: app.clear_form,

        // Function to toggle dropdown
        toggle_drop: app.toggle_drop,

        // Functions for org management
        create_group : app.create_group,
        select_group : app.select_group,

        // Functions for adding members
        toggle_add_member : app.toggle_add_member,
        add_member : app.add_member
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
        
        axios.get(load_groups_url).then(function(response) {
            app.vue.groups=app.enumerate(response.data.groups);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
