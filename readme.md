# Staticlyh

Extremely basic static site generation for posts, converting Markdown to HTML. Created since I thought it would be a simple enough exercise.

## How it works

Supply some markdown files and a html page template, and then the script converts your file into valid HTML and places it into a copy of the template, ensuring every page looks the same across your posts.

## How to use

1. In your website folder, create a `_posts` folder containing all your `.md` files. (You can have subfolders 1 level deep in here)
    * Markdown files should be titled in the format `YYYY-MM-DD-title-goes-here.md`
    * You can skip the date but this reduces the variables you can use later (see `--dateof`)
    * Any spaces will be converted to `-` for the final built files

2. Create the same folder structure but with `posts` instead of `_posts` (Script currently doesn't create the output directory on its own)
3. Create a `posts.htemplate` file containing the layout of your page
    You can use the following variables inside this template file:

    | Variable | Usage                                                                 |
    | -------- | --------------------------------------------------------------------- |
    | --title  | Uses the first line of the Markdown file                              |
    | --text   | The contents of the Markdown file are placed here (Converted to HTML) |
    | --dateof | Adds the date of the Markdown file from the filename (if it exists)   |
    | --year   | Uses the current year                                                 |

4. For each subfolder inside your `_posts` folder, you may create a template page that links to all pages within it named after the folder (e.g `./_posts/blogs` becomes `./blogs.html` on the root using `blogs.htemplate`).
    * If you are not using subfolders inside `_posts`, then create the file `.htemplate` on the root
        * You can *only* do this if not using subfolders!
        * The output page will be called `posts.html`

5. To create each entry link on such a page, you need to tell Staticlyh what part of the HTML page to duplicate and fill in. Below is an example for a `blogs.htemplate` like above:

    ```html
        <main>
            --/
            <section>
                <a href="--path"><h2>--title</h2></a>
                <time>Posted on: --dateof</time>
                <p>--description</p>
                <hr>
            </section>
            /--
        </main>
    ```

    Notice the use of `--/ /--` around the part that needs to be duplicated, and the variable names. Staticlyh will paste everything between `--/ /--` right underneath until every page has been referenced.

    You can use the following variables inside this template file:

    | Variable       | Usage                                                                                                                |
    | -------------- | -------------------------------------------------------------------------------------------------------------------- |
    | --title        | Uses the first line of the referenced Markdown file                                                                  |
    | --path         | Puts in the final file path of the referenced page                                                                   |
    | --description  | The first 200 characters of the referenced Markdown file are placed here, converted to HTML and removing any headers |
    | --dateof       | Adds the date of the referenced Markdown file from the filename (if it exists)                                       |
    | --year         | Uses the current year                                                                                                |

6. Run the script with `./staticlyh.py build /path/to/your/site/`

## Dependencies

* Python 3 (Any recent version will probably work)
* Python-Markdown (`pip install markdown`)

## Notes

* Windows style paths were not tested as I use Linux.
* This is probably not the best tool for the job if you want a proper website of your own, as this requires a very specific website setup and many parts of your website still need to be copy-pasted around. Consider trying out something like [Jekyll](https://jekyllrb.com/) or similar. This was just made for fun! Feel free to use it though if you really want to...

## AI Disclaimer

None used!
