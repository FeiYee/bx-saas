
rm -rf dist
mkdir dist

cp -r deploy/* dist/

cp -r server/* dist/server
rm -rf dist/server/__pycache__
rm -rf dist/server/*/__pycache__
rm -rf dist/server/*/*/__pycache__
rm -rf dist/server/*/*/*/__pycache__
rm -rf dist/server/cache/
rm -rf dist/server/asset/
mkdir dist/server/cache/
mkdir dist/server/asset/

cd website
npm run generate
cp -r dist/* ../dist/website/www
cd ..

cd admin
npm run build
cp -r dist/* ../dist/admin/www
cd ..

cd graph
npm run build
cp -r dist/* ../dist/graph/www
cd ..

cd medical
npm run build
cp -r dist/* ../dist/medical/www
cd ..


# cd doc
# mkdocs build
# cp -r site/* ../dist/doc/www
# cd ..
