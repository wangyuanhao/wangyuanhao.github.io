(function () {
  'use strict';

  var content = document.getElementById('blog-content');
  if (!content) return;

  // Count Chinese characters separately so mixed-language notes get a useful estimate.
  var text = content.textContent || '';
  var chinese = text.match(/[\u3400-\u9fff]/g) || [];
  var words = text.replace(/[\u3400-\u9fff]/g, ' ').match(/\S+/g) || [];
  var readingTime = document.querySelector('[data-reading-time]');
  if (readingTime) readingTime.textContent = Math.max(1, Math.ceil(chinese.length / 400 + words.length / 200));

  var headings = content.querySelectorAll('h1, h2, h3');
  var toc = document.querySelector('[data-blog-toc]');
  var root = document.createElement('ul');
  var stack = [{ level: 0, list: root }];

  headings.forEach(function (heading, index) {
    var title = heading.textContent;
    if (!heading.id) {
      var id = 'section-' + (index + 1);
      while (document.getElementById(id)) id += '-section';
      heading.id = id;
    }
    var href = '#' + encodeURIComponent(heading.id);
    var level = Number(heading.tagName.slice(1));
    while (stack.length > 1 && level < stack[stack.length - 1].level) stack.pop();
    var parent = stack[stack.length - 1];
    if (level > parent.level && parent.list.lastElementChild) {
      var nested = document.createElement('ul');
      parent.list.lastElementChild.appendChild(nested);
      stack.push({ level: level, list: nested });
    } else if (stack.length === 1) {
      parent.level = level;
    }
    var item = document.createElement('li');
    var link = document.createElement('a');
    link.href = href;
    link.textContent = title;
    item.appendChild(link);
    stack[stack.length - 1].list.appendChild(item);

    var anchor = document.createElement('a');
    anchor.href = href;
    anchor.className = 'blog-heading-anchor';
    anchor.textContent = '#';
    anchor.setAttribute('aria-label', '链接到：' + title);
    heading.appendChild(anchor);
  });

  if (toc && headings.length) {
    toc.querySelector('nav').appendChild(root);
    toc.hidden = false;
  }
}());
