<template>
    <v-container grid-list-md>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="login-card">
            <v-card-title>
              <span class="headline">Pay For {{items[0].loan_fund_details.type}}</span>
            </v-card-title>

            <v-spacer/>

            <v-card-text>

              <v-layout
                row
                fill-height
                justify-center
                align-center
                v-if="loading"
              >
                <v-progress-circular
                  :size="50"
                  color="primary"
                  indeterminate
                />
              </v-layout>


              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>

                  <v-text-field
                    v-model="credentials.amount"
                    :counter="70"
                    label="amount"
                    :value="this.items[0].pwt"
                    :rules="rules.amount"
                    type="number"
                    step=".01"
                    maxlength="70"
                    required
                  />

                </v-container>
                <v-btn class="green white--text" :disabled="!valid" @click="apply">Pay</v-btn>

              </v-form>


            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
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
        <template v-for="(item, index) in pre_payments">
          <v-list-item :to="item.link" :key="item.id">
            
            <template v-slot:default="{ active }">
              <v-list-item-content>
                <v-list-item-title v-text="items[0].loan_fund_details.name"></v-list-item-title>

                <v-list-item-subtitle
                  class='text--primary'
                >{{ item.date | formatDate }}</v-list-item-subtitle>

                <v-list-item-subtitle >{{"The Payment amount was "+ item.amount}}</v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action>
                <v-list-item-action-text>{{items[0].loan_fund_details.interest_rate + "%"}}</v-list-item-action-text>

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
    </v-container>
    
</template>

<script>
import axios from 'axios';
import router from "../router";
import moment from "moment";


export default {
    name: "Payment",
    data() {
        return {
            selected: [0],
            credentials: {},
            valid:true,
            loading:false,
            rules: {
                amount: [
                    v => !!v || "Amount is required",
                    v => (v == this.items[0].pmt) || "The amount must be EQUAL to "+this.items[0].pmt,
                    v => /^\d+\.\d{0,2}?$/.test(v) || "can only contain digits"
                ],
            },
            items: [{ loan_fund_details : {type : "FD"}}],
            pre_payments: [],
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
        }else{
            const AuthStr = 'JWT '.concat(this.$session.get("token"))
            //console.log(this.$session.get('user'))
            const pk = this.$route.params.id;
            axios.get('http://localhost:8000/application/'+pk, { headers: { Authorization: AuthStr }}).then(res => {
                    console.log(res.data)
                    this.items = [res.data]
                    this.pre_payments = res.data.payment_details
                    var interest = (Number(res.data.loan_fund_details.interest_rate)/100)/12;
                    console.log(interest)
                    var amount = Number(res.data.amount);
                    var duration = Number(res.data.loan_fund_details.duration);

                    var pmt = (interest*amount)/(1-Math.pow((1+interest), (-1*duration)));
                    pmt = Number(pmt).toFixed(2)
                    console.log(pmt)
                    this.items[0].pmt = pmt
                }).catch(e => {
                    this.loading = false;
                    console.log("error")
                    this.$swal({
                    type: 'warning',
                    title: 'Error',
                    text: 'Something went wrong',
                    showConfirmButton:false,
                    showCloseButton:false,
                    timer:3000
                    })
                })
        }
    },
    apply() {
          // checking if the input is valid
            if (this.$refs.form.validate()) {
                this.loading = true;
                const AuthStr = 'JWT '.concat(this.$session.get("token"))
                

                this.credentials["date"] = new Date()
                this.credentials["amount"] = this.items[0].pmt
                this.credentials["application"]  = this.items[0].id

                console.log(this.credentials)

                axios.post('http://localhost:8000/payment', this.credentials, { headers: { Authorization: AuthStr }}).then(res => {
                    router.push('/');
                }).catch(e => {
                    this.loading = false;
                    this.$swal({
                    type: 'warning',
                    title: 'Error',
                    text: 'Wrong amount entered',
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
<style lang="css" scoped>
.stackSheet {
    position: relative;
}
.stackSpark {
    position: absolute;
    top: 0;
    left: 0;
}
</style>