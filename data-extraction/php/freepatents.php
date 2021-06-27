<?php
header("Content-Type: application/rss+xml; charset=UTF-8");
$xml = new SimpleXMLElement('<rss/>');
$xml->addAttribute("version", "2.0");

function formatXml($simpleXMLElement)
{
    $xmlDocument = new DOMDocument('1.0');
    $xmlDocument->preserveWhiteSpace = false;
    $xmlDocument->formatOutput = true;
    $xmlDocument->loadXML($simpleXMLElement->asXML());

    return $xmlDocument->saveXML();
}

$channel = $xml->addChild("channel");

$channel->addChild("title", "Free Patents");
$channel->addChild("link", "http://localhost");
$channel->addChild("description", "Free Patents Feed");
$channel->addChild("language", "en-us");

$url = "https://www.freepatentsonline.com/result.html?p=1&edit_alert=&srch=xprtsrch&query_txt=AGT%2FScholl+and+AGT%2FMatthias&uspat=on&date_range=last20&stemming=on&sort=chron&search=Search";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_CAINFO, __DIR__ . DIRECTORY_SEPARATOR . 'cacert.pem');

$output = curl_exec($ch);

$patent_links = [];
$entries = [];

if ($output === false) {
    die(curl_error($ch));
} else {

    libxml_use_internal_errors(true);

    $dom = new DOMDocument();
    $dom->preserveWhiteSpace = false;
    $dom->formatOutput = true;
    $dom->loadHTML($output);
    

    $xpath = new DOMXPath($dom);

    $nodeList = $xpath->query('//table[@class="listing_table"]//tr[position()>1]/td[3]/a');

    foreach ($nodeList as $tr) {
        $patent_links[] = 'https://www.freepatentsonline.com' . $tr->getAttribute('href');
    }

    foreach ($patent_links as $patent_link) {
        curl_setopt($ch, CURLOPT_URL, $patent_link);
        $output = curl_exec($ch);
        if ($output === false) {
            die($patent_link . " is giving HTTP error");
        } else {
            $dom->loadHTML($output);
            $xpath = new DOMXPath($dom);

            $docTypeAndNumber = trim($xpath->query('//div[@class="disp_doc2"][2]/div[@class="disp_elm_text"]')->item(0)->nodeValue);
            $title = trim($xpath->query('//div[text()="Title:"]/following-sibling::div')->item(0)->nodeValue);
            $inventors = trim(preg_replace("/\(.+\)/", "", $xpath->query('//div[text()="Inventors:"]/following-sibling::div')->item(0)->nodeValue));
            $publicationDate = trim(preg_replace("/\(.+\)/", "", $xpath->query('//div[text()="Publication Date:"]/following-sibling::div')->item(0)->nodeValue));
            $filingDate = trim(preg_replace("/\(.+\)/", "", $xpath->query('//div[text()="Filing Date:"]/following-sibling::div')->item(0)->nodeValue));

            $entries[] = [
                'title' => $title,
                'description' => "Document Type and Number: $docTypeAndNumber \n Inventors: $inventors \n Publication Date: $publicationDate \n Filing Date: $filingDate",
                'link' => $patent_link
            ];
        }
    }

    foreach ($entries as $entry) {
        $item = $channel->addChild("item");

        $item->addChild("title", $entry['title']);
        $item->addChild("link", $entry['link']);
        $item->addChild("description", $entry['description']);
    }

    echo formatXml($xml);

    libxml_clear_errors();
}
curl_close($ch);