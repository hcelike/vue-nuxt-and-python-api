import { merge, pick, keys, startCase, camelCase} from 'lodash'

export function getUrlParameter(sParam) {
  let sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=')
    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined
        ? true
        : decodeURIComponent(sParameterName[1])
    }
  }
}

export function mergeKeys(old, newO) {
  merge(old, pick(newO, keys(old)))
}

export function formatDate(timestamp){
  let date = new Date(timestamp);
  return date.toLocaleString('en', {
          year: "numeric",
          month: "2-digit",
          day: "numeric"
      })
}

export function formatDateLong(timestamp) {
  let date = new Date(timestamp);
  return date.toLocaleString('en')
}

export function  titleCase(str) {
  try {
    return startCase(camelCase(str));
  } catch (e) {
    return str;
  }
}

export function format_number(n) {
  const options = {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }

  return Number(n).toLocaleString('en', options)
}
