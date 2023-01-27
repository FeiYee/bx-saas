
rm -rf dist
mkdir dist

cp -r deploy/* dist/

cp -r server/* dist/server
rm -rf dist/server/__pycache__
rm -rf dist/server/*/__pycache__
rm -rf dist/server/*/*/__pycache__
rm -rf dist/server/*/*/*/__pycache__

cd client
npm run build
cp -r dist/* ../dist/client/www
cd ..

cd portal
npm run build
cp -r dist/* ../dist/portal/www
cd ..

cd website
npm run build
cp -r dist/* ../dist/website/www
cd ..

# cd doc
# mkdocs build
# cp -r site/* ../dist/doc/www
# cd ..
