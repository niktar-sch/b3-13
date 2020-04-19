class TopLevelTag:

    is_single = False
    text = ""
    content = [] #(indent, text)
    attrs = {}
    klass = ()

    def __init__(self, tag, **attrs):
        self.tag = tag
        self.klass = attrs.pop("klass", ())
        self.attrs = attrs
        self.text = ""
        self.content = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iadd__(self, other):
        for (indent, tag) in other.get_tag_list():
            self.content.append((indent + 1, tag))
        return self

    def get_attrs(self):
        result = ""
        if self.klass:
            result += f" class=\"{' '.join(self.klass)}\""
        result += "".join(f" {k.replace('_', '-')}=\"{v}\"" for k, v in self.attrs.items())
        return result

    def get_tag_list(self):
        if self.is_single:
            result = [(0, f"<{self.tag}{self.get_attrs()}/>")]
        else:
            if self.content:
                result = [(0, f"<{self.tag}{self.get_attrs()}>")] 
                result += self.content
                if self.text:
                    result += [(1, self.text)]
                result += [(0, f"</{self.tag}>")]
            else:
                result = [(0, f"<{self.tag}{self.get_attrs()}>{self.text}</{self.tag}>")]
        return result


class Tag(TopLevelTag):

    def __init__(self, tag, **attrs):
        TopLevelTag.__init__(self, tag, **attrs)
        self.is_single = self.attrs.pop("is_single", False)


class HTML(TopLevelTag):

    tag = "html"
    
    def __init__(self, output=None):
        self.output = output
        self.content = [] #(indent, text)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.output:
            with open(self.output, "w") as f:
                for indent, val in self.get_tag_list():
                    print(f"{'  '*indent}{val}", file=f)
        else:
            for indent, val in self.get_tag_list():
                print(f"{'  '*indent}{val}")

    def __iadd__(self, other):
        for (indent, tag) in other.get_tag_list():
            self.content.append((indent, tag))
        return self


if __name__ == "__main__":

    #Тестовый код со станицы (добавлена отсутствующая запятая перед data_image="responsive")
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

            body += div

        doc += body


    #Тестовый код по ссылке на GitHub (отсутствует параметр ata_image="responsive")
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body