<template>
  <v-card
    class="mx-auto"
  >
    <v-toolbar
      color="pink"
      dark
    >
    
    

      <v-toolbar-title>Avaibale Loan Funds</v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-checkbox-marked-circle</v-icon>
      </v-btn> -->
    </v-toolbar>

    <v-list two-line>
      <v-list-item-group
        v-model="selected"
        active-class="pink--text"
        multiple
      >
        <template v-for="(item, index) in items">
          <v-list-item :to="item.link" :key="item.id">
            
            <template v-slot:default="{ active }">
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>

                <v-list-item-subtitle
                  class='text--primary'
                >{{ item.duration | duration }}</v-list-item-subtitle>

                <v-list-item-subtitle >{{"The Application Should be between "+ item.min_amount+" and " +item.max_amount}}</v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action>
                <v-list-item-action-text>{{item.interest_rate + "%"}}</v-list-item-action-text>

                <v-icon
                  v-if="!active"
                  color="grey lighten-1"
                >
                  mdi-star-outline
                </v-icon>

                <v-icon
                  v-else
                  color="yellow darken-3"
                >
                  mdi-star
                </v-icon>
              </v-list-item-action>
            </template>
          </v-list-item>

          <v-divider
            v-if="index < items.length - 1"
            :key="index"
          ></v-divider>
        </template>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
import axios from 'axios';
import swal from 'sweetalert2';
import router from "../router";
export default {
    name: "LoanFund",
    data() {
        return {
            selected: [0],
            items: [],
        };
    },
    mounted() {
        this.checkLoggedIn();
    },
    methods: {
    checkLoggedIn() {
        this.$session.start();
        
        if (!this.$session.has("token")) {
            router.push("/auth");
            if(this.$session.get("user")[0].is_superuser){
              router.push("/admin");
            }
        }else{
            const AuthStr = 'JWT '.concat(this.$session.get("token"))
            console.log(this.$session.get('user'))
            axios.get('http://localhost:8000/loan-fund', { headers: { Authorization: AuthStr }}).then(res => {
                    console.log(res.data)
                    this.items = res.data
                    this.items.forEach( appl => {
                      appl["link"] = "/loan/"+appl.id
                    });
                }).catch(e => {
                    this.loading = false;
                    console.log("error")
                    swal({
                    type: 'warning',
                    title: 'Error',
                    text: 'Wrong username or password',
                    showConfirmButton:false,
                    showCloseButton:false,
                    timer:3000
                    })
                })
        }
    }
    }
};
</script>
