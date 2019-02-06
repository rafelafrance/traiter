////////////////////////////////////////////////////////////////////////////////////
// Data passed in from python

const None = null;
const True = true;
const False = false;

const allRows = {{ rows | safe }};
const args = {{ args | safe }};
const as_is = {{ as_is | safe }};

////////////////////////////////////////////////////////////////////////////////////

const SPAN_OPEN = '<span class="found">';
const SPAN_CLOSE = '</span>';

function buildTable(page) {
  const begin = (page - 1) * pageSize;
  const end   = page * pageSize;
  const rows = allRows.slice(begin, end);
  const tbody = document.querySelector('tbody');

  while (tbody && tbody.firstChild) { // Remove old rows
    tbody.removeChild(tbody.firstChild);
  }

  rows.forEach(row => {
    const tr = document.createElement('tr');

    let td = document.createElement('td');
    td.innerHTML = row.index;
    tr.appendChild(td);

    args.extra_field.forEach(field => {
      td = document.createElement('td');
      td.innerHTML = row.raw[field];
      tr.appendChild(td);
    });

    args.trait.forEach(field => {
      td = document.createElement('td');
      td.innerHTML = formatParsedField(row, field);
      tr.appendChild(td);
    });

    args.search_field.forEach(field => {
      td = document.createElement('td');
      td.innerHTML = formatSearchdField(row, field);
      tr.appendChild(td);
    });

    as_is.forEach(field => {
      td = document.createElement('td');
      td.innerHTML = `${SPAN_OPEN}${row.raw[field]}${SPAN_CLOSE}`;
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
}

function formatSearchdField(row, field) {
  if (row.formattedSearchField && row.formattedSearchField[field]) {
    return row.formattedSearchField[field];
  }

  const green = 1;
  const white = 0;

  parts = row.raw[field].split('');
  colors = (new Array(parts.length + 1)).fill(white);

  Object.keys(row.parsed).forEach(key => {
    row.parsed[key]
      .filter(parse => parse.field == field)
      .forEach(parse => {
        for (let i = parse.start; i < parse.end; ++i) {
          colors[i] = green;
        }
      });
  });

  for (let i = colors.length - 2; i > 0; --i) {
    if (colors[i] == colors[i + 1]) {
      continue;
    }
    if (colors[i] == green) {
      parts.splice(i + 1, 0, SPAN_CLOSE)
    } else {
      parts.splice(i + 1, 0, SPAN_OPEN)
    }
  }
  if (colors.length && colors[0] == green) {
    parts.splice(0, 0, SPAN_OPEN)
  }

  row.formattedSearchField = row.formattedSearchField || {};
  row.formattedSearchField[field] = parts.join('');
  return row.formattedSearchField[field];
}

function formatParsedField(row, field) {
  if (row.formattedParsedField && row.formattedParsedField[field]) {
    return row.formattedParsedField[field];
  }

  const lines = [];

  row.parsed[field].forEach((trait, t) => {
    if (t) lines.push('<hr/>');
    if (trait.value) lines.push(`value: ${trait.value}`);
    if (trait.units) lines.push(`original units: ${trait.units}`);
    if (trait.field) lines.push(`field: ${trait.field}`);
    if (trait.start) lines.push(`start: ${trait.start}`);
    if (trait.end) lines.push(`end: ${trait.end}`);
    Object.keys(trait.flags).forEach(flag => {
      let flagValue;
      if (trait.flags[flag] === true) {
        flag = flag.replace('_', ' ');
        lines.push(`${flag}`);
      } else {
        flagValue = trait.flags[flag].replace('_', ' ');
        flag = flag.replace('_', ' ');
        lines.push(`${flag}: ${flagValue}`);
      }
    });
  });

  row.formattedParsedField = row.formattedParsedField || {};
  row.formattedParsedField[field] = lines.join('<br/>');
  return row.formattedParsedField[field];
}

////////////////////////////////////////////////////////////////////////////////////
// Pager logic

var pageSize = 100;
var maxPage;

function changePage() {
  const pager = document.querySelector('.pager');
  var page = +pager.value;
  page = page < 1 ? 1 : page;
  page = page > maxPage ? maxPage : page;
  pager.value = page;
  buildTable(page);
}

document.querySelector('.first-page').addEventListener('click', function() {
  const pager = document.querySelector('.pager');
  pager.value = 1;
  changePage();
});

document.querySelector('.previous-page').addEventListener('click', function() {
  const pager = document.querySelector('.pager');
  pager.value = +pager.value - 1;
  changePage();
});

document.querySelector('.next-page').addEventListener('click', function() {
  const pager = document.querySelector('.pager');
  pager.value = +pager.value + 1;
  changePage();
});

document.querySelector('.last-page').addEventListener('click', function() {
  const pager = document.querySelector('.pager');
  pager.value = maxPage;
  changePage();
});

document.querySelector('.pager').addEventListener('change', changePage);

function resetPager() {
  maxPage = Math.ceil(allRows.length / pageSize);
  document.querySelector('.max-page').innerHTML = 'of ' + maxPage;
  document.querySelector('.pager').value = '1';
  changePage();
}

resetPager();
