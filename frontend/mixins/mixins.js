import {startCase, camelCase} from 'lodash';

export default {

methods: {
    makeCopy(x) {
      return JSON.parse( JSON.stringify(x) );
    },
    toTitleCase(str) { 
      try {
        return startCase(camelCase(str));
      } catch (e) {
        return str;
      }
    },
    prettyOptionDate(expiration_date){
      const shortMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      if (expiration_date) {
        expiration_date = new Date(expiration_date);
        let monthIndex = expiration_date.getMonth()
        let monthStr = shortMonths[monthIndex].toUpperCase();
        let yearStr = expiration_date.getFullYear().toString().substr(-2);
        let dayStr = expiration_date.getDate();
        expiration_date = `${monthStr} ${dayStr} '${yearStr}`;
      }
      return expiration_date;
    },
    toUsersTimeZone(date) {
      try {
        let deserializedDate = new Date(date);
        let currentTimeZoneOffset = deserializedDate.getTimezoneOffset() * 60_000;
        return new Date(deserializedDate - currentTimeZoneOffset);
      } catch (e) {
        return date;
      }
    },
    formatInstrument(item, type) {
      let formatted = null;
      if (item.security_type == "STK") {
        formatted = this.formatStock(item);
      } 
      else if (item.security_type == "OPT") {
        if ( type == 'simple' ) {
          formatted = this.formatOptionSimple(item);
        } else {
          formatted = this.formatOption(item);
        }
      }
      else if (item.security_type == "AGG") {
        formatted = this.formatStock(item);
      }
      return formatted;
    }, 
    formatOptionSimple(item) {
      return `${this.prettyOptionDate(item.expiration_date)} ${item.strike} ${item.right}`; 
    },
    formatOption(item) {
      return `${item.symbol} ${this.prettyOptionDate(item.expiration_date)} ${item.strike} ${item.right}`; 
    },
    formatStock(item) {
      return `${item.symbol}`;
    },
    toRounded(x) {
      try {
        return x.toFixed(2)
      } catch(e) {
        return x;
      }
    },
    toCurrency(num, n=2 ){
       var x = null;
       var re = "\\d(?=(\\d{" + (x || 3) + "})+" + (n > 0 ? "\\." : "$") + ")";
       try {
           num = parseFloat(num);
       } catch(e){
       }  
       try {
           if (isNaN(num)) {
             return '--';
           } 
           return (
           "$" + num.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, "g"), "$&,")
           );
       } catch (e) {
           return num;
       }
    },
    formatDate(timestamp){
        var date = new Date(timestamp);
        return date.toLocaleString('en', {
                year: "numeric",
                month: "2-digit",
                day: "numeric"
            })
    },
    formatDateLong(timestamp){
        var date = new Date(timestamp);
        return date.toLocaleString('en')
    },
    toPercent(num) {
        let x = null;
        let n = 2;
        let re = "\\d(?=(\\d{" + (x || 3) + "})+" + (n > 0 ? "\\." : "$") + ")";
        try {
          num = num * 100;
          return (
            num.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, "g"), "$&,") + "%"
          );
        } catch (e) {
          return num;
        }
    }
  }
};
