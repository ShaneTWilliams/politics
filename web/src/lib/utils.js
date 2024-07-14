export function formatNumber(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function formatString(x) {
    return x.toString().replace("--", "–");
}
