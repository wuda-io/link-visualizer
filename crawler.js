const url = require("url");

const baseUrl = "https://wuda.io";

function findLinks(html) {
  var anchors = /<a\s[^>]*?href=(["']?)([^\s]+?)\1[^>]*?>/gi;
  var links = [];
  html.replace(anchors, function (_anchor, _quote, url) {
    links.push(url);
  });

  const newLinks = links.map((l) => {
    return url.resolve(baseUrl, l);
  });

  newLinks.sort();

  return newLinks;
}

fetch(baseUrl)
  .then((resp) => resp.text())
  .then((text) => {
    //console.log(text);
    const urls = findLinks(text);
    console.log(urls);
  });
