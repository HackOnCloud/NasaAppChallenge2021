export async function fetchData(length = 10) {
  const limit = 2 * length; // get double the requested posts because some don't have images
  const res = await fetch(
    `https://www.reddit.com/r/dogswithjobs/.json?limit=${limit}`
  );
  const dogs = [];
  const { data } = await res.json();
  data.children.forEach((c) => {
    const title = c.data.title;
    const url = c.data.preview?.images[0]?.resolutions[2]?.url;
    const id = c.data.id;
    if (url) {
      dogs.push({ id, title: title, url: url.replaceAll("&amp;", "&") });
    }
  });
  return dogs.slice(0, length);
}
