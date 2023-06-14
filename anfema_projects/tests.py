from django.test import TestCase
from . models import AnfemaProject
from django.http import JsonResponse
import time

# Create your tests here.

# method for creating new anfema project entries
def create_anfema_project_entry(title, meta_first_published_at, client, subtitle, brand_main_colour):
    return AnfemaProject.objects.create(title=title, meta_first_published_at=meta_first_published_at, client=client, subtitle=subtitle, brand_main_colour=brand_main_colour)

# tests for view.last_update
class AnfemaProjectLastUpdateViewTests(TestCase):
        
    def test_last_update_with_no_entries(self):
        response = self.client.get('/anfema-projects/last-update/')
        
        self.assertContains(response, "no entries found")
        self.assertEqual(response.status_code, 200)
        
        
    def test_last_update_with_one_entry(self):
        create_anfema_project_entry(title="test", meta_first_published_at="2023-06-13", client="test", subtitle="test", brand_main_colour="test")
        response = self.client.get('/anfema-projects/last-update/')
        self.assertContains(response, "test")
        self.assertEqual(response.status_code, 200)
    
    
    def test_last_update_with_two_entries(self):
        create_anfema_project_entry(title="test1", meta_first_published_at="2023-06-13", client="test1", subtitle="test1", brand_main_colour="test1")
        #wait for 1 millisecond to make sure that the updated_at field is different
        time.sleep(0.001)
        create_anfema_project_entry(title="test2", meta_first_published_at="2023-06-13", client="test2", subtitle="test2", brand_main_colour="test2")
        response = self.client.get('/anfema-projects/last-update/')
    
        self.assertContains(response, "test2")
        self.assertEqual(response.status_code, 200)
        
        #change test1 subtitle to test1.1 -> test1 should be the last updated entry
        #wait for 1 millisecond to make sure that the updated_at field is different
        time.sleep(0.001)
        test1 = AnfemaProject.objects.get(title="test1")
        test1.subtitle = "test1.1"
        test1.save()
        response = self.client.get('/anfema-projects/last-update/')
        
        self.assertContains(response, "test1")
        self.assertEqual(response.status_code, 200)
            
# tests for view.perform_update
class AnfemaProjectPerformUpdateTests(TestCase):
    
    # test for perform_update with no header => should have saved all 10 entries in the database
    def test_perform_update_with_no_header(self):
        response = self.client.post("http://localhost:8000/anfema-projects/perform-update/")
        self.assertEqual(response.status_code, 202)
        # time.sleep(3)
        self.assertEqual(AnfemaProject.objects.count(), 10)
        
    # test for perform_update with header "X-OLDER-THAN 2022-09-28T18:00:34.781852+02:00" => should have saved 5 entries in the database
    def test_perform_update_with_header(self):
        response = self.client.post("http://localhost:8000/anfema-projects/perform-update/", HTTP_X_OLDER_THAN="2022-09-28T18:00:34.781852+02:00")
        self.assertEqual(response.status_code, 202)
        # time.sleep(3)
        self.assertEqual(AnfemaProject.objects.count(), 5)
    
    
    