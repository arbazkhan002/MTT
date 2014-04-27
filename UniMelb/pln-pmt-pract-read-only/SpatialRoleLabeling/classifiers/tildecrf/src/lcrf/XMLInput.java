/**
 * 
 */
package lcrf;

import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.FactoryConfigurationError;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import lcrf.logic.Atom;
import lcrf.logic.Interpretation;
import lcrf.logic.NumberConstant;
import lcrf.logic.Term;
import lcrf.logic.TermSchema;
import lcrf.logic.Variable;
import lcrf.logic.parser.AtomParser;
import lcrf.logic.parser.ParseException;
import lcrf.stuff.Pair;

import org.apache.log4j.Logger;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/**
 * @author bgutmann
 * 
 */
public class XMLInput {
    public static Pair<List<List<Atom>>,List<String>> readSequencesDOM(String filename) {
        assert filename != null;

        Document document = null;
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(filename);
        } catch (FactoryConfigurationError e) {
            Logger.getLogger(XMLInput.class).error("unable to get a document builder factory");
        } catch (ParserConfigurationException e) {
            Logger.getLogger(XMLInput.class).error("parser was unable to be configured");
        } catch (SAXException e) {
            Logger.getLogger(XMLInput.class).error("parsing error");
        } catch (IOException e) {
            Logger.getLogger(XMLInput.class).error("i/o error");
        }

        Element documentElement = document.getDocumentElement();

        assert documentElement.getTagName().equals("sequences");

        NodeList sequenceNodes = documentElement.getElementsByTagName("sequence");
        List<List<Atom>> sequences = new Vector<List<Atom>>(sequenceNodes.getLength(), 5);
        List<String> sequenceIDs = new Vector<String>(sequenceNodes.getLength(), 5);

        for (int i = 0; i < sequenceNodes.getLength(); i++) {
            
            NodeList atomNodes = ((Element) sequenceNodes.item(i)).getElementsByTagName("atom");
            List<Atom> sequence = new Vector<Atom>(atomNodes.getLength(), 5);
            for (int j = 0; j < atomNodes.getLength(); j++) {
                String name = atomNodes.item(j).getTextContent().trim();
                try {
                    sequence.add(new Atom(name));
                } catch (ParseException e) {
                    Logger.getLogger(XMLInput.class).error("Parse exception at atom " + name);
                    Logger.getLogger(XMLInput.class).error(e.getStackTrace());
                }
            }
            sequences.add(sequence);
            String id = ((Element) (sequenceNodes.item(i))).getAttribute("id");
            sequenceIDs.add(id);
        }

        Pair<List<List<Atom>>,List<String>> result = new Pair<List<List<Atom>>,List<String>>(sequences,sequenceIDs);
        return result;
    }
    
    
    public static InterpretationExampleContainer readInterpreationExamplesDOM(String filename) {
        assert filename != null;

        Document document = null;
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(filename);
        } catch (FactoryConfigurationError e) {
            Logger.getLogger(XMLInput.class).error("unable to get a document builder factory");
        } catch (ParserConfigurationException e) {
            Logger.getLogger(XMLInput.class).error("parser was unable to be configured");
        } catch (SAXException e) {
            Logger.getLogger(XMLInput.class).error("parsing error");
        } catch (IOException e) {
            Logger.getLogger(XMLInput.class).error("i/o error");
        }

        Element documentElement = document.getDocumentElement();

        assert documentElement.getTagName().equals("data");
        
        Element classAtomsElement = (Element) documentElement.getElementsByTagName("classatoms").item(0);
        NodeList classAtom = classAtomsElement.getElementsByTagName("atom");

        Vector<Atom> classAtoms = new Vector<Atom>();

        for (int i = 0; i < classAtom.getLength(); i++) {
            String name = classAtom.item(i).getTextContent().trim();
            try {
                classAtoms.add(new Atom(name));
            } catch (ParseException e) {
                Logger.getLogger(XMLInput.class).error("Parse exception at classatom " + name);
                Logger.getLogger(XMLInput.class).error(e.getStackTrace());
            }
        }
        
        NodeList sequenceNodes = documentElement.getElementsByTagName("sequence");

        InterpretationExampleContainer container = new InterpretationExampleContainer(sequenceNodes.getLength(), classAtoms);

        for (int i = 0; i < sequenceNodes.getLength(); i++) {
            String sequenceid = ((Element)(sequenceNodes.item(i))).getAttribute("id");            
            NodeList positionNodes = ((Element) sequenceNodes.item(i)).getElementsByTagName("pos");                       
                                
            List<Interpretation> insequence = new Vector<Interpretation>(positionNodes.getLength());
            List<Atom> outsequence = new Vector<Atom>(positionNodes.getLength());

            for (int j = 0; j < positionNodes.getLength(); j++) {                
                String label = ((Element) ((Element) positionNodes.item(j)).getElementsByTagName("label").item(0)).getTextContent().trim();
                try {
                    outsequence.add(new Atom(label));
                } catch (ParseException e) {
                    Logger.getLogger(XMLInput.class).error("Parse exception at atom " + label);
                    Logger.getLogger(XMLInput.class).error(e.getStackTrace());
                }

                
                
                NodeList interpretationNodes =  ((Element) positionNodes.item(j)).getElementsByTagName("entry");                
                
                Interpretation inter = new Interpretation(interpretationNodes.getLength());
                
                for (int k=0; k<interpretationNodes.getLength(); k++) {
                    
                    String tmp = ((Element) interpretationNodes.item(k)).getTextContent().trim();                    
                    try {
                        inter.add(new Atom(tmp));
                    } catch (ParseException e) {
                        Logger.getLogger(XMLInput.class).error("Parse exception at atom " + tmp);
                        Logger.getLogger(XMLInput.class).error(e.getStackTrace());
                    }                   
                }
                insequence.add(inter);
                                                
            }
            container.addExample(insequence, outsequence,sequenceid);
        }

        return container;
    }

    
    

    public static SimpleExampleContainer readInOutExamplesDOM(String filename) {
        assert filename != null;

        Document document = null;
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(filename);
        } catch (FactoryConfigurationError e) {
            Logger.getLogger(XMLInput.class).error("unable to get a document builder factory");
        } catch (ParserConfigurationException e) {
            Logger.getLogger(XMLInput.class).error("parser was unable to be configured");
        } catch (SAXException e) {
            Logger.getLogger(XMLInput.class).error("parsing error");
        } catch (IOException e) {
            Logger.getLogger(XMLInput.class).error("i/o error");
        }

        Element documentElement = document.getDocumentElement();

        assert documentElement.getTagName().equals("data");

        NodeList sequenceNodes = documentElement.getElementsByTagName("sequence");
        Element classAtomsElement = (Element) documentElement.getElementsByTagName("classatoms").item(0);
        NodeList classAtom = classAtomsElement.getElementsByTagName("atom");

        Vector<Atom> classAtoms = new Vector<Atom>();

        for (int i = 0; i < classAtom.getLength(); i++) {
            String name = classAtom.item(i).getTextContent().trim();
            try {
                classAtoms.add(new Atom(name));
            } catch (ParseException e) {
                Logger.getLogger(XMLInput.class).error("Parse exception at classatom " + name);
                Logger.getLogger(XMLInput.class).error(e.getStackTrace());
            }

        }

        SimpleExampleContainer container = new SimpleExampleContainer(sequenceNodes.getLength(), classAtoms);

        for (int i = 0; i < sequenceNodes.getLength(); i++) {
            NodeList inputNodes = ((Element) ((Element) sequenceNodes.item(i)).getElementsByTagName("input")
                    .item(0)).getElementsByTagName("entry");
            NodeList outputNodes = ((Element) ((Element) sequenceNodes.item(i))
                    .getElementsByTagName("output").item(0)).getElementsByTagName("entry");
            assert inputNodes.getLength() == outputNodes.getLength();

            List<Atom> insequence = new Vector<Atom>(inputNodes.getLength());
            List<Atom> outsequence = new Vector<Atom>(outputNodes.getLength());

            for (int j = 0; j < inputNodes.getLength(); j++) {
                String inname = inputNodes.item(j).getTextContent().trim();
                String outname = outputNodes.item(j).getTextContent().trim();
                try {
                    insequence.add(new Atom(inname));
                } catch (ParseException e) {
                    Logger.getLogger(XMLInput.class).error("Parse exception at atom " + inname);
                    Logger.getLogger(XMLInput.class).error(e.getStackTrace());
                }
                try {
                    outsequence.add(new Atom(outname));
                } catch (ParseException e) {
                    Logger.getLogger(XMLInput.class).error("Parse exception at atom " + outname);
                    Logger.getLogger(XMLInput.class).error(e.getStackTrace());
                }
            }
            container.addExample(insequence, outsequence);
        }

        return container;
    }

    public static List<TermSchema> readSchemata(String filename) {
        assert filename != null;

        Document document = null;
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(filename);
        } catch (FactoryConfigurationError e) {
            Logger.getLogger(XMLInput.class).error("unable to get a document builder factory");
        } catch (ParserConfigurationException e) {
            Logger.getLogger(XMLInput.class).error("parser was unable to be configured");
        } catch (SAXException e) {
            Logger.getLogger(XMLInput.class).error("parsing error");
        } catch (IOException e) {
            Logger.getLogger(XMLInput.class).error("i/o error");
        }

        Element documentElement = document.getDocumentElement();
        // documentElement.tagName == "schemata"

        NodeList schemaNodes = documentElement.getElementsByTagName("schema");
        List<TermSchema> schemata = new Vector<TermSchema>(schemaNodes.getLength());

        for (int i = 0; i < schemaNodes.getLength(); i++) {
            try {
                schemata.add(parseSchemaElement((Element) schemaNodes.item(i)));
            } catch (Exception e) {
                Logger.getLogger(XMLInput.class).error(
                        "Error at Parsing the schema-Element :\n" + schemaNodes.item(i) + "\n" + e);
            }
        }

        return schemata;
    }

    public static TermSchema parseSchemaElement(Element el) throws Exception {
        assert el != null;
        String strSchemaTerm = el.getElementsByTagName("schematerm").item(0).getTextContent();
        AtomParser parser = new AtomParser(new StringReader(strSchemaTerm));

        Term schemaTerm = parser.Term();
        
           //TODO make it better, with user settable types!
        for (Variable vintern:schemaTerm.getContainedVariables()) {            
            vintern.setVariableType(schemaTerm.hashCode()*vintern.hashCode());
        }
        

        int schemaType = 0;

        if (el.hasAttribute("type")) {
            String type = el.getAttribute("type").toLowerCase();
            if (type.contains("input")) {
                schemaType &= WindowMaker.FIELDINPUT;
            } else if (type.contains("output")) {
                schemaType &= WindowMaker.FIELDOUTPUT;
            } else if (type.contains("diverse")) {
                schemaType &= WindowMaker.FIELDDIVERSE;
            } else if (type.contains("all")) {
                schemaType = 0;
            } else {
                throw new RuntimeException("Unknown Schematype " + type);
            }
        } else {
            Logger.getLogger(XMLInput.class).info("No type specified for schema, use input");
            schemaType = WindowMaker.FIELDINPUT;
        }

        HashMap<Variable, List<Term>> h = new HashMap<Variable, List<Term>>(schemaTerm
                .getContainedVariables().size() + 2);

        NodeList substitutions = el.getElementsByTagName("substitutions");

        for (int i = 0; i < substitutions.getLength(); i++) {
            Element elSubstitutions = (Element) substitutions.item(i);

            String variableStr = elSubstitutions.getAttribute("variable");
            parser.ReInit(new StringReader(variableStr));
            Term variableTerm = parser.Term();

            if (!(variableTerm instanceof Variable)) {
                throw new Exception("Only variables can be substituted.");
            }
            
            Variable v = (Variable) variableTerm;
            
         
            //Logger.getLogger(XMLInput.class).info(schemaTerm + " " + v + " " +v.getVariableType());

            List<Term> possibleSubstitutions = new Vector<Term>();

            NodeList entryElements = elSubstitutions.getElementsByTagName("entry");
            for (int j = 0; j < entryElements.getLength(); j++) {
                String entryString = ((Element) entryElements.item(j)).getTextContent();
                parser.ReInit(new StringReader(entryString));
                possibleSubstitutions.add(parser.Term());
            }

            NodeList numberConstantElements = elSubstitutions.getElementsByTagName("numberconstant");
            for (int j = 0; j < numberConstantElements.getLength(); j++) {
                int from = Integer.parseInt(((Element) numberConstantElements.item(j)).getAttribute("from")
                        .trim());
                int to = Integer.parseInt(((Element) numberConstantElements.item(j)).getAttribute("to")
                        .trim());

                for (int k = from; k <= to; k++) {
                    possibleSubstitutions.add(new NumberConstant(k));
                }
            }
            
            if (elSubstitutions.getElementsByTagName("boundedvar").getLength() > 0) 
                possibleSubstitutions.add(new Variable(TermSchema.BOUNDEDVAR));
            
            if (elSubstitutions.getElementsByTagName("unboundedvar").getLength() > 0) 
                possibleSubstitutions.add(new Variable(TermSchema.UNBOUNDEDVAR));

            h.put(v, possibleSubstitutions);
        }

        // add idendity for variables that have no substitutions
        for (Variable v : schemaTerm.getContainedVariables()) {
            if (!h.containsKey(v)) {
                List<Term> possibleSubstitutions = new Vector<Term>(1);
                possibleSubstitutions.add(v);
                h.put(v, possibleSubstitutions);
            }
        }

        return new TermSchema(schemaTerm, h, schemaType);
    }

    public static SimpleExampleContainer readInOutExamplesSAX(String filename) {
        class MySAXHandler extends DefaultHandler {
            private AtomParser parser;

            private boolean inputSequenceMode;

            private String content;

            public SimpleExampleContainer container;

            private Vector<Atom> classAtoms;

            private Vector<Atom> input;

            private Vector<Atom> output;
            
            private String id;

            public MySAXHandler() {
                classAtoms = new Vector<Atom>();
                content = "";

                parser = new AtomParser(new StringReader("42"));
                try {
                    parser.Term();
                } catch (ParseException e) {
                    throw new RuntimeException("P=NP!");
                }

            }

            public void startElement(String uri, String localName, String qName, Attributes attributes)
                    throws SAXException {
                if (qName.equals("sequence")) {
                    id = attributes.getValue("id");
                    input = new Vector<Atom>();
                    output = new Vector<Atom>();
                } else if (qName.equals("input")) {
                    inputSequenceMode = true;
                } else if (qName.equals("output")) {
                    inputSequenceMode = false;
                }

                content = "";
            }

            public void endElement(String uri, String localName, String qName) throws SAXException {
                if (qName.equals("atom")) {
                    try {
                        parser.ReInit(new StringReader(content));
                        classAtoms.add(new Atom(parser.Term()));
                    } catch (ParseException e) {
                        throw new SAXException("Error at parsing atom.\n" + e.getMessage());
                    }
                } else if (qName.equals("entry")) {
                    try {
                        parser.ReInit(new StringReader(content));
                        Atom a = new Atom(parser.Term());
                        if (inputSequenceMode) {
                            input.add(a);
                        } else {
                            output.add(a);
                        }
                    } catch (ParseException e) {
                        throw new SAXException("Error at parsing atom.\n" + e.getMessage());
                    }
                } else if (qName.equals("classatoms")) {
                    container = new SimpleExampleContainer(classAtoms);

                } else if (qName.equals("sequence")) {
                    container.addExample(input, output);

                }
            }

            public void characters(char[] ch, int start, int length) throws SAXException {
                content = content.concat(new String(ch, start, length));
            }

            public void ignorableWhitespace(char[] ch, int start, int length) throws SAXException {}

            public void startDocument() throws SAXException {}

            public void endDocument() throws SAXException {}
        }

        MySAXHandler handler = new MySAXHandler();
        try {
            // Use the default (non-validating) parser
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser saxParser = factory.newSAXParser();
            saxParser.parse(new File(filename), handler);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            e.printStackTrace();
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        }
        return handler.container;
    }

    public static WindowMaker makeWindowMakerWithBGKnowledge(String filename, int windowSize) {
        assert filename != null;

        Document document = null;
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(filename);
        } catch (FactoryConfigurationError e) {
            Logger.getLogger(XMLInput.class).error("unable to get a document builder factory");
        } catch (ParserConfigurationException e) {
            Logger.getLogger(XMLInput.class).error("parser was unable to be configured");
        } catch (SAXException e) {
            Logger.getLogger(XMLInput.class).error("parsing error");
        } catch (IOException e) {
            Logger.getLogger(XMLInput.class).error("i/o error");
        }

        Element documentElement = document.getDocumentElement();

        assert documentElement.getTagName().equals("backgroundknowledge");

        String prologpart = documentElement.getElementsByTagName("prolog").item(0).getTextContent().trim();
        NodeList featureNodes = documentElement.getElementsByTagName("feature");
        Vector<String> featureNames = new Vector<String>();
        for (int i = 0; i < featureNodes.getLength(); i++) {
            featureNames.add(((Element) featureNodes.item(i)).getAttribute("name").trim());
        }

        return new WindowMaker(windowSize, prologpart, featureNames);
    }

}
