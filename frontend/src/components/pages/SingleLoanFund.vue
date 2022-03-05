<template>
    <v-container grid-list-md>
    <div class="row mt-5">
    <div class="col">
        <h1 class="text-center">Amoritization Table for {{items[0].max_amount}}$</h1>
    </div>
    </div>
    <div class="row mt-5" v-if="arrRemain.length > 0">
    <div class="col">
        <h2 class="text-center">Remaing</h2>
        <bar-chart
        :chartData="arrRemain"
        :options="chartOptions"
        :chartColors="RemainChartColors"
        label="Balance"
        />
    </div>
    </div>

    <div class="row mt-5" v-if="arrPrincipal.length > 0">
        <div class="col">
        <h2 class="text-center">Principal</h2>
        <bar-chart
            :chartData="arrPrincipal"
            :options="chartOptions"
            :chartColors="PrincipalChartColors"
            label="Principal"
        />
        </div>
    </div>

    <div class="row mt-5" v-if="arrInterest.length > 0">
        <div class="col">
            <h2 class="text-center">Interest</h2>
            <bar-chart
                :chartData="arrInterest"
                :options="chartOptions"
                :chartColors="interestColors"
                label="Interest"
            />
        </div>
    </div>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="login-card">
            <v-card-title>
              <span class="headline">Apply For {{items[0].type}}</span>
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
                    :rules="rules.amount"
                    type="number"
                    maxlength="70"
                    required
                  />

                </v-container>
                <v-btn class="green white--text" :disabled="!valid" @click="apply">Apply</v-btn>

              </v-form>


            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
    
</template>

<script>
import axios from 'axios';
import router from "../../router";
import moment from "moment";
import BarChart from "@/components/BarChart.vue";


export default {
    name: "SingleLoanFund",
    components: {
        BarChart
    },
    data() {
        return {
            selected: [0],
            credentials: {},
            valid:true,
            loading:false,
            rules: {
                amount: [
                    v => !!v || "Amount is required",
                    v => (v <= this.items[0].max_amount) || "The amount must be smaller than or equal to "+this.items[0].max_amount,
                    v => (v >= this.items[0].min_amount) || "The amount must be bigger than or equal to"+this.items[0].min_amount,
                    v => /^\d+$/.test(v) || "can only contain digits"
                ],
            },
            items: [{max_amount : 9850000}],
            arrRemain: [],
            RemainChartColors: {
                borderColor: "#077187",
                pointBorderColor: "#0E1428",
                pointBackgroundColor: "#AFD6AC",
                backgroundColor: "#74A57F"
            },
            arrPrincipal: [],
            PrincipalChartColors: {
                borderColor: "#251F47",
                pointBorderColor: "#260F26",
                pointBackgroundColor: "#858EAB",
                backgroundColor: "#858EAB"
            },
            arrInterest: [],
            interestColors: {
                borderColor: "#190B28",
                pointBorderColor: "#190B28",
                pointBackgroundColor: "#E55381",
                backgroundColor: "#E55381"
            },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false
            }
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
            console.log(this.$session.get('user'))
            const pk = this.$route.params.id;
            axios.get('http://localhost:8000/loan-fund/'+pk, { headers: { Authorization: AuthStr }}).then(res => {
                console.log(res.data)
                this.items = [res.data]
                var interest = (Number(res.data.interest_rate)/100)/12;
                console.log(interest)
                var amount = Number(res.data.max_amount);
                var duration = Number(res.data.duration);

                var pmt = (interest*amount)/(1-Math.pow((1+interest), (-1*duration))); //  total payment each period
                console.log(Number(pmt).toFixed(2))
                var last_month = (pmt*36)-amount;
                var remaining = amount;
                const date = new Date()

                for(var i = 0; i < res.data.duration; i++){
                    var int_amount = remaining*interest;
                    var principal_amount = pmt-int_amount;
                    remaining = remaining - principal_amount;
                    date.setMonth(date.getMonth() + 1)
                    const date_format = moment(date, "YYYYMMDD").format("MM/YY");
                    //console.log(date_format)
                    if(i == res.data.duration -1){
                        this.arrRemain.push({ date_format, total: remaining })
                        this.arrInterest.push({ date_format, total: int_amount })
                        this.arrPrincipal.push({ date_format, total: principal_amount })
                    }else{
                        this.arrRemain.push({ date_format, total: remaining })
                        this.arrInterest.push({ date_format, total: int_amount })
                        this.arrPrincipal.push({ date_format, total: principal_amount })
                    }
                }
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
                this.credentials["start_date"] = new Date()
                this.credentials["loan_fund"] = this.items[0].id
                this.credentials["user"]  = this.$session.get("user")[0].id

                axios.post('http://localhost:8000/application', this.credentials, { headers: { Authorization: AuthStr }}).then(res => {
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